"""App EntryPoint."""
import time

from fastapi import Cookie, Depends, FastAPI, Request
from typing import Annotated, Optional

from web_app.models.user import User
from web_app.routers import account
from web_app.services.auth_service import AuthService

app = FastAPI()

app.include_router(account.router)

@app.get("/{numero}")
async def read_root(
    request: Request,
    numero: int,
    session_id: Optional[str] = Cookie(default=None)
):
    """Root app API showing query params, path, and cookies."""
    # raise Exception("F en el chat")
    # time.sleep(120)
    return {
        "numero": numero,
        "host": request.headers.get("host"),
        "path": str(request.url.path),
        "query_params": dict(request.query_params),
        "cookies": request.cookies,
        "session_id": session_id,
        "message": "Welcome to my FastAPI application!"
    }



@app.get("/whoami")
async def read_loan(
    current_user: Annotated[User, Depends(AuthService.get_authenticated_user)],
):
    """Get Loan only for lender or borrower."""
    return {
        "message": f"Yo soy {current_user.id_num} y mi email es {current_user.email}"
    }
