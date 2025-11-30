from datetime import datetime
from uuid import UUID as TypeUUID

from sqlalchemy import TIMESTAMP, UUID, Boolean, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.root_model import Base
from src.utils.generators import generate_uuid


# Class to handle the User
class User(Base):
    __tablename__ = "User"
    user_id: Mapped[TypeUUID] = mapped_column(
        UUID, primary_key=True, default=generate_uuid
    )
    user_email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now,
        nullable=False,
    )
