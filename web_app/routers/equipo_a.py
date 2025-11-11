"""Router - Account CRUD."""
from typing import Annotated

from fastapi import APIRouter, Depends

from web_app.models.user import User
from web_app.database import SessionDep
from web_app.schemas.token import Token
from web_app.schemas.user import UserCreate, UserRead
from web_app.services.auth_service import AuthService
from web_app.services.user_service import UserService

router = APIRouter(prefix="/equipoa", tags=["TeamA"])



@router.get("/whoami")
async def whoami(
    current_user: Annotated[User, Depends(AuthService.get_authenticated_user)],
):
    """Show user."""
    return {
        "message": f"EQUIPO A1: Yo soy {current_user.user_id} y mi email es {current_user.email}"
    }

@router.post("/whoami2/{id_nevera}")
async def whoami2(
    id_nevera: int,
    # leer el json.
    current_user: Annotated[User, Depends(AuthService.get_authenticated_user)],
):
    """todavia no sabemos que responder."""
    return {
        "message": f"EQUIPO A2: Yo soy {current_user.user_id} y mi email es {current_user.email} - id-nevera {id_nevera}"
    }
