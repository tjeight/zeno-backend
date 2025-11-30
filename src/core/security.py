from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Function to hash a password"""
    return password_context.hash(password)


def verify_password(raw_password: str, hashed_password) -> bool:
    """Function to verify a password"""
    return password_context.verify(raw_password, hashed_password)
