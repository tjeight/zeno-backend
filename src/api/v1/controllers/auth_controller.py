from src.db.repositories.user_repo import get_user_by_email
from src.services.auth_service import register_user_service


async def user_register_controller(payload, db):
    """Controller function to handle the register user"""
    return await register_user_service(db, payload)


async def user_get_controller(payload, db):
    """Controller function to handle get user"""
    return await get_user_by_email(payload, db)
