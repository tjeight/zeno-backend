from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt
from src.core.settings import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Function to hash a password"""
    return password_context.hash(password)


def verify_password(raw_password: str, hashed_password) -> bool:
    """Function to verify a password"""
    return password_context.verify(raw_password, hashed_password)


def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    """Function to create the access token"""

    #  copy the data
    to_encode = data.copy()

    #  create the expiry time
    expiry_time = datetime.now() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # add the expiry time
    to_encode["exp"] = expiry_time

    # get the algorithm
    algorithm = settings.ALGORITHM

    # settings key
    secret_key = settings.SECRET_KEY

    #  encode the data
    access_token = jwt.encode(
        claims=to_encode,
        key=secret_key,
        algorithm=algorithm,
    )

    return access_token


def create_refresh_token(data: dict, expires_minutes: int | None = None) -> str:
    # get the data
    to_encode: dict = data.copy()

    #  get the expiry time
    expiry_time = datetime.now() + timedelta(
        minutes=expires_minutes or settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    # add the expiry time
    to_encode["exp"] = expiry_time

    # secret key
    secret_key = settings.SECRET_KEY

    #  get the algorithm
    algorithm = settings.ALGORITHM

    # encode
    refresh_token = jwt.encode(claims=data, key=secret_key, algorithm=algorithm)

    return refresh_token
