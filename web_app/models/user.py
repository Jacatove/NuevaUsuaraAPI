"""Models."""
# pylint: disable=unsubscriptable-object
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from web_app.models.base import Base



class User(Base):  # pylint: disable=too-few-public-methods
    """User table model."""

    __tablename__ = "users"

    id_num: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    def __repr__(self) -> str:
        """Return a string representation of the User."""
        return (
            f"id_num={self.id_num!r}, "
            f"email={self.email!r} "
        )
