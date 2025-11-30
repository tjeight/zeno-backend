from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

from src.db.base import Base
from src.core.settings import settings  # <-- loads your .env

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


print("DATABASE_URL =>", settings.DATABASE_URL)

target_metadata = Base.metadata


def get_sync_url():
    """
    Convert async URL to sync URL for Alembic.
    """
    url = settings.DATABASE_URL  # <-- read from your .env via settings.py
    return url.replace("postgresql+asyncpg://", "postgresql+psycopg://")


def run_migrations_offline():
    url = get_sync_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    sync_url = get_sync_url()

    connectable = engine_from_config(
        {"sqlalchemy.url": sync_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
