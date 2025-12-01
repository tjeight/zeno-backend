from src.db.repositories.user_repo import create_user, get_user_by_email
from src.core.security import hash_password
from src.models.user_model import User


async def register_user_service(db, payload):
    # hash password
    hashed = hash_password(payload.password)

    # build user object
    user = User(
        user_email=payload.email,
        hashed_password=hashed,
    )

    return await create_user(db, user)


async def get_user_service(db, payload):
    await get_user_by_email(db=db, email=payload.email)
