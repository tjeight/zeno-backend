from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.schemas.user_schema import LoginSchema, UserCreate
from src.db.repositories.user_repo import create_user, get_user_by_email
from src.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from src.models.user_model import User
from fastapi import HTTPException, status


async def register_user_service(db: AsyncSession, payload: UserCreate):
    # hash password
    hashed = hash_password(payload.password)

    # check the if user already exists
    existing_user = await get_user_by_email(db, payload.email)
    if existing_user:
        raise ValueError("User with this email already exists")

    # build user object
    user = User(
        user_email=payload.email,
        hashed_password=hashed,
    )

    return await create_user(db, user)


async def login_user_service(db: AsyncSession, payload: LoginSchema) -> tuple[str, str]:
    #  get the user by email
    user = await get_user_by_email(db, payload.email)

    if not user:
        raise ValueError("Invalid email or password")

    #  verify password
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # create token
    access_token = create_access_token(data={"sub": str(user.user_id)})
    # refresh token
    refresh_token = create_refresh_token(data={"sub": str(user.user_id)})

    return access_token, refresh_token
