from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.expense import Expense


async def create_expense(db: AsyncSession, title: str, amount: float):
    expense = Expense(title=title, amount=amount)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


async def list_expenses(db: AsyncSession):
    result = await db.execute(select(Expense))
    return result.scalars().all()
