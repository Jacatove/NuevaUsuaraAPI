"""Schemas for otp."""
from pydantic import BaseModel


class OtpValidate(BaseModel):
    """User creation data."""

    otp_code: str
