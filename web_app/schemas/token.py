"""Schema for Token."""
from pydantic import BaseModel, Field


class TokenData(BaseModel):
    """TokenData schema."""

    username: str | None = None


class Token(BaseModel):
    """Token schema."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
