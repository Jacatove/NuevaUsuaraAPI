"""Schemas for User/Account."""
from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    """User creation data."""

    email: EmailStr
    password: str
    id_num: int

class UserRead(BaseModel):
    """User read schema."""

    email: EmailStr
    id_num: int

    class Config:  # pylint: disable=too-few-public-methods
        """Config for UserRead."""

        orm_mode = True
        from_attributes = True
