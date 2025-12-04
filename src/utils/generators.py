from secrets import token_urlsafe

from uuid6 import UUID, uuid7


def generate_uuid() -> UUID:
    """This is the helper function to generate the uuid for the database"""
    return uuid7()


def generate_refresh_token() -> str:
    """
    Generates a cryptographically secure raw refresh token.
    RAW token goes to the cookie, HASH goes to the DB.
    """
    return token_urlsafe(64)
