from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_model import User


async def create_user(db: AsyncSession, user: User):
    """Repo function to add the user"""
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    """Repo function to get the user by email"""
    statement = select(User).where(User.user_email == email)
    result = await db.execute(statement)
    return result.scalars().first()
