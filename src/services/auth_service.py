from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.user_schema import LoginSchema, UserCreate
from src.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from src.db.repositories.refresh_token_repo import (
    get_refresh_token_by_hash,
    invalidate_refresh_token,
    save_refresh_token_to_db,
)
from src.db.repositories.user_repo import create_user, get_user_by_email
from src.models.user_model import User
from src.utils.generators import generate_refresh_token


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


async def login_user_service(
    db: AsyncSession,
    payload: LoginSchema,
) -> tuple[str, str]:
    # 1. Get user
    user = await get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # 2. Verify password
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # 3. Create access token (JWT)
    access_token = create_access_token({"sub": str(user.user_id)})

    # 4. Create refresh token (random string, NOT JWT)
    raw_refresh_token = generate_refresh_token()

    # 5. Hash refresh token for DB
    refresh_hash = hash_refresh_token(raw_refresh_token)

    # 6. Save hashed refresh token in DB
    await save_refresh_token_to_db(
        db=db,
        user_id=user.user_id,
        token_hash=refresh_hash,
    )

    # 7. Return access + RAW refresh token
    # (raw refresh will go to the cookie in the route layer)
    return access_token, raw_refresh_token


async def refresh_token_service(db: AsyncSession, refresh_token: str):
    # hash incoming refresh token
    hashed = hash_refresh_token(refresh_token)

    # retrieve token row from DB
    token_row = await get_refresh_token_by_hash(db, hashed)
    if not token_row or not token_row.is_valid:
        raise ValueError("Invalid or expired refresh token")

    # ---- TOKEN ROTATION ----
    # 1. Invalidate old refresh token
    await invalidate_refresh_token(db, hashed)

    # 2. Create a new refresh token for rotation
    new_raw_token = generate_refresh_token()
    new_hashed_token = hash_refresh_token(new_raw_token)

    # 3. Store new refresh token
    await save_refresh_token_to_db(
        db=db,
        user_id=token_row.user_id,
        token_hash=new_hashed_token,
    )

    # Issue new access token
    new_access = create_access_token({"sub": str(token_row.user_id)})

    return new_access, new_raw_token
