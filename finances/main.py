from typing import Literal, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
import asyncpg
import asyncio

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

# Database connection pool
DATABASE_URL = 'postgresql://nekoneki:nekoneki@aee050d48b5d840129b4408248c78a00-143447042.eu-north-1.elb.amazonaws.com:5432/expenses_db'
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    # Create the database and table if they don't exist
    async with pool.acquire() as connection:
        # Create the 'expenses' table if it doesn't exist
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                destination TEXT NOT NULL,
                amount NUMERIC NOT NULL,
                currency VARCHAR(3) NOT NULL
            )
        ''')

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await pool.close()

@app.post("/expenses/")
async def create_expense(expense: Expense):
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                'INSERT INTO expenses(destination, amount, currency) VALUES($1, $2, $3)',
                expense.destination, expense.amount, expense.currency
            )
    return {"message": "Expense recorded", "expense": expense}

@app.get("/expenses/")
async def get_expenses() -> List[Expense]:
    async with pool.acquire() as connection:
        rows = await connection.fetch('SELECT * FROM expenses')
        return [{"destination": row["destination"], "amount": row["amount"], "currency": row["currency"]} for row in rows]
