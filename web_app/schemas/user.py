"""Schemas for User/Account."""
from pydantic import BaseModel, EmailStr, UUID4


class UserCreate(BaseModel):
    """User creation data."""

    email: EmailStr
    password: str


class UserRead(BaseModel):
    """User read schema."""

    email: EmailStr
    user_id: UUID4

    class Config:  # pylint: disable=too-few-public-methods
        """Config for UserRead."""

        orm_mode = True
        from_attributes = True
