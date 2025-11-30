from uuid6 import uuid7, UUID


def generate_uuid() -> UUID:
    """This is the helper function to generate the uuid for the database"""
    return uuid7()
