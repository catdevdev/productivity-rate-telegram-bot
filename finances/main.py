from typing import Literal, List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query
from fastapi.logger import logger
import asyncpg
from datetime import datetime, date

# Initialize the FastAPI application
app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight": False,
        "syntaxHighlight.theme": "obsidian",
        "deepLinking": False
    }
)

# Define the Pydantic model for individual expense input
class Expense(BaseModel):
    destination: str = Field(..., example="Groceries")
    amount: float = Field(..., example=100.0)
    currency: Literal['USD', 'EUR', 'UAH'] = Field(..., example='UAH')

# Define the Pydantic model for the output, including ID and timestamp
class ExpenseOutput(Expense):
    id: int
    created_at: datetime

# Define the Pydantic model for a wrapper object containing a list of expenses
class ExpenseArrayWrapper(BaseModel):
    expenses: List[Expense]

class DeleteExpensesRequest(BaseModel):
    expense_ids: List[int] = Field(..., example=[1, 2, 3])

# Define the Pydantic model for the successful delete response
class DeleteExpensesResponse(BaseModel):
    message: str = Field(..., example="Expenses with ids [1, 2, 3] deleted successfully, count: 3")

# Database connection pool
DATABASE_URL = 'postgresql://nekoneki:nekoneki@a2794a54deb1c4f1bac4d5dfc8590d37-1520523198.eu-north-1.elb.amazonaws.com:5432/expenses_db'
pool = None

# Initialize the database connection pool
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

# Event handler to initialize the database on application startup
@app.on_event("startup")
async def on_startup():
    await init_db()

# Event handler to close the database connection pool on application shutdown
@app.on_event("shutdown")
async def on_shutdown():
    await pool.close()

# POST endpoint to create multiple expenses
@app.post("/expenses/", response_model=List[ExpenseOutput])
async def create_expenses(expense_data: ExpenseArrayWrapper):
    created_expenses = []
    async with pool.acquire() as connection:
        async with connection.transaction():
            for expense in expense_data.expenses:
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

# GET endpoint to retrieve expenses, optionally filtering by date
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

# DELETE endpoint to delete multiple expenses
@app.delete("/expenses/", response_model=DeleteExpensesResponse)
async def delete_expenses(delete_request: DeleteExpensesRequest):
    try:
        async with pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.execute(
                    'DELETE FROM expenses WHERE id = ANY($1::int[])',
                    delete_request.expense_ids
                )
                deleted_count = int(result.split(' ')[1])
                if deleted_count == 0:
                    raise HTTPException(status_code=404, detail="No expenses found to delete")
        return {"message": f"Expenses with ids {delete_request.expense_ids} deleted successfully, count: {deleted_count}"}
    except HTTPException as e:
        logger.error(f"HTTP error during deletion: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Server error occurred while deleting expenses.")

