from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_db
from src.api.v1.schemas.expense_schema import ExpenseCreate
from src.services.expense_service import (
    add_expense_service,
    get_expenses_service,
)


async def create_expense_controller(
    payload: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
):
    return await add_expense_service(db, payload)


async def list_expenses_controller(
    db: AsyncSession = Depends(get_db),
):
    return await get_expenses_service(db)
