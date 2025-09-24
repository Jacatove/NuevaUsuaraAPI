"""Authentication service module."""
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from web_app.config import settings
from web_app.database import SessionDep
from web_app.schemas.token import Token, TokenData
from web_app.services.user_service import UserService
from web_app.utils import create_access_token, oauth2_scheme, verify_password


class AuthService:
    """Service for authentication."""

    @staticmethod
    async def authenticate_user(
        session: SessionDep,
        form_data: OAuth2PasswordRequestForm,
    ) -> Token:
        """
        Authenticate user and return access token.

        Args:
            form_data (OAuth2PasswordRequestForm): Login credentials.

        Returns:
            Token: Access token and metadata.

        Raises:
            HTTPException: If credentials are invalid or account is locked.
        """
        user = await UserService.get_user_by_email(
            session,
            form_data.username,
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        # Update last login
        user.last_login = datetime.now()
        session.commit()

        access_token = create_access_token(
            data={
                "sub": user.email,
            },
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )

    @staticmethod
    async def get_authenticated_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: SessionDep, 
    ):
        """
        TODO: pending.

        determine it is is appropiate to call this function
        to get user in other requests.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError as exc:
            raise credentials_exception from exc
        user = await UserService.get_user_by_email(
            session,
            token_data.username,
        )
        if user is None:
            raise credentials_exception
        return user
