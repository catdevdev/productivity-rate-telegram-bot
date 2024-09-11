from typing import List
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import asyncpg
from datetime import datetime, date

app = FastAPI()

class Expense(BaseModel):
    destination: str = Field(..., example="Groceries")
    amount: float = Field(..., example=100.0)
    currency: str = Field(..., example='UAH')

class ExpenseOutput(Expense):
    id: int
    created_at: datetime

class ExpenseArrayWrapper(BaseModel):
    expenses: List[Expense]

class DeleteExpensesRequest(BaseModel):
    expense_ids: List[int] = Field(..., example=[1, 2, 3])

class DeleteExpensesResponse(BaseModel):
    message: str = Field(..., example="Expenses with ids [1, 2, 3] deleted successfully, count: 3")

DATABASE_URL = 'postgresql://nekoneki:nekoneki@a2794a54deb1c4f1bac4d5dfc8590d37-1520523198.eu-north-1.elb.amazonaws.com:5432/expenses_db'
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
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
    if pool:
        await pool.close()

@app.delete("/expenses/", response_model=DeleteExpensesResponse)
async def delete_expenses(delete_request: DeleteExpensesRequest):
    if not delete_request.expense_ids:
        raise HTTPException(status_code=400, detail="No expense IDs provided.")
    try:
        async with pool.acquire() as connection:
            async with connection.transaction():
                # Execute the delete statement and capture the number of affected rows
                result = await connection.execute(
                    'DELETE FROM expenses WHERE id = ANY($1::int[])',
                    delete_request.expense_ids
                )
                # Extract the number of rows deleted
                deleted_count = int(result.split(' ')[-1]) if result.startswith('DELETE') else 0
                if deleted_count == 0:
                    raise HTTPException(status_code=404, detail="No expenses found to delete")
    except Exception as e:
        # Log the error (use logging if configured for real-world apps)
        print(f"Error during deletion: {e}")
        raise HTTPException(status_code=500, detail="Internal server error. Unable to delete expenses.")
    return {"message": f"Expenses with ids {delete_request.expense_ids} deleted successfully, count: {deleted_count}"}
