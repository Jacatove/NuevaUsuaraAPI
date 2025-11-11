"""Router - Account CRUD."""
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from web_app.database import SessionDep
from web_app.schemas.token import Token
from web_app.schemas.user import UserCreate, UserRead
from web_app.services.auth_service import AuthService
from web_app.services.user_service import UserService

router = APIRouter(prefix="/account", tags=["account"])


@router.post(
        "/signup",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: UserCreate,
    session: SessionDep,
):
    """
    Register a new user.

    Args:
        user (UserCreate): pydantic model containing required data to
          create a User.

    Returns:
        UserRead: pydantic model containing the created user's details.
    """
    return await UserService.create_user(session, user)


@router.post("/signin", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    """
    Authenticate to get access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Login credentials.

    Returns:
        Token: Access token and metadata.

    Raises:
        HTTPException: If credentials are invalid.
    """
    return await AuthService.authenticate_user(session, form_data)
