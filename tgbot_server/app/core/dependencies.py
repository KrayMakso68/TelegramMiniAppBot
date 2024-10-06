import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import configs
from app.core.database import get_async_session
from app.core.exceptions import JwtCredentialsError, IsActiveUserError
from app.core.security import oauth_scheme
from app.schema.auth_schema import TokenData
from app.schema.user_schema import UserSchema
from app.services.auth_service import AuthService
from app.repository.user_repository import UserRepository


# user
async def get_current_user(token: str = Depends(oauth_scheme),
                           user_repository: UserRepository = Depends(UserRepository)
                           ) -> UserSchema:
    try:
        payload = jwt.decode(token, configs.JWT_SECRET_KEY, algorithms=[configs.ALGORITHM])
        tg_id: int = payload.get("tg_id")
        if tg_id is None:
            raise JwtCredentialsError("Could not validate credentials", {"WWW-Authenticate": "Bearer"})

        token_data = TokenData(tg_id=tg_id)
    except InvalidTokenError:
        raise JwtCredentialsError("Could not validate credentials", {"WWW-Authenticate": "Bearer"})
    user: UserSchema | None = await user_repository.get_by_tg_id(token_data.tg_id)
    if user is None:
        raise JwtCredentialsError("Could not validate credentials", {"WWW-Authenticate": "Bearer"})
    return user


async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)) -> UserSchema:
    if not current_user.is_active:
        raise IsActiveUserError("Inactive user")
    return current_user


def get_user_repository(async_session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(async_session)


# auth
def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)
