from typing import Literal, List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query
import asyncpg
from datetime import datetime, date

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight": False,
        "syntaxHighlight.theme": "obsidian",
        "deepLinking": False
    }
)

# Define the Pydantic model for expense input
class Expense(BaseModel):
    destination: str = Field(..., example="Groceries")
    amount: float = Field(..., example=100.0)
    currency: Literal['USD', 'EUR', 'UAH'] = Field(..., example='UAH')

# Define the Pydantic model for expense output
class ExpenseOutput(Expense):
    id: int
    created_at: datetime

# Database connection pool
DATABASE_URL = 'postgresql://nekoneki:nekoneki@a2794a54deb1c4f1bac4d5dfc8590d37-1520523198.eu-north-1.elb.amazonaws.com:5432/expenses_db'
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    # Create the database and table if they don't exist
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                destination TEXT NOT NULL,
                amount NUMERIC NOT NULL,
                currency VARCHAR(3) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        ''')

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await pool.close()

# Corrected POST endpoint to accept a direct list of Expense objects
@app.post("/expenses/", response_model=List[ExpenseOutput])
async def create_expenses(expenses: List[Expense]):
    created_expenses = []
    async with pool.acquire() as connection:
        async with connection.transaction():
            for expense in expenses:
                row = await connection.fetchrow(
                    '''
                    INSERT INTO expenses(destination, amount, currency)
                    VALUES($1, $2, $3)
                    RETURNING id, destination, amount, currency, created_at
                    ''',
                    expense.destination, expense.amount, expense.currency
                )
                created_expenses.append(dict(row))
    return created_expenses

@app.get("/expenses/", response_model=List[ExpenseOutput])
async def get_expenses(expense_date: Optional[date] = Query(None, description="Filter expenses by date")) -> List[ExpenseOutput]:
    async with pool.acquire() as connection:
        if expense_date:
            rows = await connection.fetch(
                '''
                SELECT * FROM expenses 
                WHERE DATE(created_at) = $1 
                ORDER BY created_at DESC
                ''', 
                expense_date
            )
        else:
            rows = await connection.fetch('SELECT * FROM expenses ORDER BY created_at DESC')
        return [dict(row) for row in rows]

@app.delete("/expenses/{expense_id}", response_model=dict)
async def delete_expense(expense_id: int):
    async with pool.acquire() as connection:
        result = await connection.execute(
            'DELETE FROM expenses WHERE id = $1', expense_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": f"Expense with id {expense_id} deleted"}
