from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.security import oauth_scheme
from app.services.auth_service import AuthService
from app.repository.user_repository import UserRepository


# user
def get_current_user(
        token: Annotated[str, Depends(oauth_scheme)]
):
    ...


def get_user_repository(async_session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(async_session)


# auth
def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)
