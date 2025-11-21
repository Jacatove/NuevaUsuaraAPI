"""App EntryPoint."""
import json
from typing import Annotated

from fastapi import Depends, FastAPI
import requests

from web_app.config import settings
from web_app.models.user import User
from web_app.routers import account, equipo_a
from web_app.schemas.otp import OtpValidate
from web_app.services.auth_service import AuthService

app = FastAPI()

app.include_router(account.router)
app.include_router(equipo_a.router)


@app.get("/whoami")
async def whoami(
    current_user: Annotated[User, Depends(AuthService.get_authenticated_user)],
):
    """Show user."""
    return {
        "message": f"Yo soy {current_user.user_id} y mi email es {current_user.email}"
    }

@app.get("/otp")
async def otp(
    current_user: Annotated[User, Depends(AuthService.get_authenticated_user)],
):
    url = f"{settings.OTP_API_URL}/otp/register"
    payload = json.dumps({
        "user_id": str(current_user.user_id)
    })
    headers = {
        'X-Key': settings.OTP_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return {
        "otpauth_url": response.json().get("otpauth_url")
    }


@app.post("/confirm-otp")
async def confirm_otp(
    otp: OtpValidate,
    current_user: Annotated[User, Depends(AuthService.get_authenticated_user)],
):
    url = f"{settings.OTP_API_URL}/otp/validate"

    payload = json.dumps({
        "user_id": str(current_user.user_id),
        "code": otp.otp_code,
    })

    headers = {
        'X-Key': settings.OTP_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        return True

    return False

