"""User service module."""
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from web_app.models.user import User
from web_app.schemas.user import UserCreate, UserRead
from web_app.utils import hash_password


class UserService:
    """Service for user management."""

    @staticmethod
    async def create_user(session: Session, user_data: UserCreate) -> UserRead:
        """
        Create a new user and the associated wallet.

        Args:
            user_data (UserCreate): User creation data.

        Returns:
            UserRead: Created user data.

        Raises:
            HTTPException: If user already exists.
        """
        stmt = select(User).where(
            (User.email == user_data.email) | (User.id_num == user_data.id_num)
        )

        existing_user = session.scalars(stmt).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or ID already exists",
            )

        new_user = User(
            id_num=user_data.id_num,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        session.add(new_user)
        session.commit()

        return UserRead.from_orm(new_user)

    @staticmethod
    async def get_user_by_email(
        session: Session,
        email: str,
    ) -> Optional[User]:
        """
        Get user by Number ID.

        Args:
            email (str): User email.

        Returns:
            Optional[User]: User if found, None otherwise.
        """
        return session.scalars(
            select(User).where(User.email == email)
        ).first()
