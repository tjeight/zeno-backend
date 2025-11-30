from fastapi import APIRouter
from src.api.v1.controllers.expense_controller import (
    create_expense_controller,
    list_expenses_controller,
)
from src.api.v1.schemas.expense_schema import ExpenseCreate, ExpenseOut

router = APIRouter(prefix="/expense", tags=["Expense"])


@router.post("/", response_model=ExpenseOut)
async def add_expense(payload: ExpenseCreate):
    return await create_expense_controller(payload)


@router.get("/", response_model=list[ExpenseOut])
async def get_expenses():
    return await list_expenses_controller()
