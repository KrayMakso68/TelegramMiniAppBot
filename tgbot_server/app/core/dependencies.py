from typing import Annotated
from fastapi import Depends

from app.core.security import oauth_scheme
from app.services.auth_service import AuthService
from app.repository.user_repository import UserRepository


def get_current_user(
        token: Annotated[str, Depends(oauth_scheme)]
):
    ...


def auth_service():
    return AuthService(UserRepository)