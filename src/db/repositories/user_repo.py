from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_model import User


async def create_user(db: AsyncSession, user: User):
    """Repo function to add the user"""
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


#  verify the identity of the user through the email and password
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Repo function to get user by email"""
    result = await db.execute(select(User).where(User.user_email == email))
    return result.scalar_one_or_none()
