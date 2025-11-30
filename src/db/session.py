from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.settings import settings

#  create a async engine for the database
engine = create_async_engine(
    settings.DATABASE_URL,
)


#  create an instance of the async session
AsyncSessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


#  create a fastapi dependency
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
