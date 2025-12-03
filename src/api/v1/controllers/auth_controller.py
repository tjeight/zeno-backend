from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.schemas.user_schema import LoginSchema
from src.db.repositories.user_repo import get_user_by_email
from src.services.auth_service import login_user_service, register_user_service


async def user_register_controller(payload, db):
    """Controller function to handle the register user"""
    return await register_user_service(db, payload)


async def user_get_controller(payload, db):
    """Controller function to handle get user"""
    return await get_user_by_email(payload, db)


async def user_login_controller(
    payload: LoginSchema, db: AsyncSession
) -> tuple[str, str]:
    """Controller function to handle user login"""

    #  get the token
    access_token, refresh_token = await login_user_service(db, payload)

    return access_token, refresh_token
