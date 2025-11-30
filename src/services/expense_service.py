from src.db.repositories.expense_repo import (
    create_expense,
    list_expenses,
)


async def add_expense_service(db, payload):
    return await create_expense(db, payload.title, payload.amount)


async def get_expenses_service(db):
    return await list_expenses(db)
