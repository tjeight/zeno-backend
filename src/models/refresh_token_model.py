# src/models/refresh_token_model.py

from datetime import datetime
from uuid import UUID as TypeUUID

from sqlalchemy import TIMESTAMP, Boolean, String, func, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.root_model import Base
from src.utils.generators import generate_uuid  # your centralized UUIDv7 generator


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    # primary id (UUIDv7, returned as uuid.UUID)
    refresh_token_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid,
        comment="primary uuid for the refresh token row",
    )

    # link to users table (note table name is 'users')
    user_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="foreign key to users.user_id",
    )

    # store hashed refresh token (never store the raw token)
    token_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        comment="hashed refresh token (e.g. HMAC or bcrypt/sha256 of token)",
    )

    user_agent: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        comment="user agent of the device/browser (optional)",
    )

    ip_address: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        comment="ip address when token was issued (optional)",
    )

    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="whether this refresh token is currently valid (revoke on logout)",
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="creation timestamp",
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="last update timestamp",
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        comment="explicit expiry (optional if you handle expiry in app logic)",
    )

    __table_args__ = (
        # quick lookups by token or user
        Index("ix_refresh_tokens_token_hash", "token_hash"),
        Index("ix_refresh_tokens_user_id", "user_id"),
    )
