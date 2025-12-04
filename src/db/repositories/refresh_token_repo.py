from sqlalchemy import select
from src.models.refresh_token_model import RefreshToken


async def get_refresh_token_by_hash(db, token_hash: str):
    statement = select(RefreshToken).where(
        RefreshToken.token_hash == token_hash, RefreshToken.is_valid
    )
    res = await db.execute(statement)
    return res.scalar_one_or_none()


async def invalidate_refresh_token(db, token_hash: str):
    token = await get_refresh_token_by_hash(db, token_hash)
    if not token:
        return None
    token.is_valid = False
    await db.commit()
    return token


async def save_refresh_token_to_db(db, user_id, token_hash):
    new_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
    )
    db.add(new_token)
    await db.commit()
    await db.refresh(new_token)
    return new_token
