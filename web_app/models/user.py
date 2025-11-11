"""Models."""
# pylint: disable=unsubscriptable-object
import uuid
import enum

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from web_app.models.base import Base


class Membership(enum.Enum):
    """Membership types."""

    FREE = "FREE"
    PREMIUM = "PREMIUM"


class User(Base):  # pylint: disable=too-few-public-methods
    """User table model."""

    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    membership: Mapped[Membership] = mapped_column(
        Enum(Membership),
        default=Membership.FREE,
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    def __repr__(self) -> str:
        """Return a string representation of the User."""
        return (
            f"user_id={self.user_id!r}, "
            f"email={self.email!r} "
        )
