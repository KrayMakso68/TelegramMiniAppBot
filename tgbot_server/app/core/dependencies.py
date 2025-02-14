from fastapi import Depends
from py3xui import AsyncApi
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_session
from app.core.exceptions import JwtCredentialsError, IsActiveUserError
from app.core.security import oauth_scheme, decode_access_token
from app.repository.payment_repository import PaymentRepository
from app.schema.auth_schema import TokenData
from app.schema.user_schema import UserSchema
from app.services.auth_service import AuthService
from app.repository.user_repository import UserRepository
from app.services.panel_service import PanelService
from app.services.payment_service import PaymentService
from app.services.subscription_service import SubscriptionService
from app.services.user_service import UserService
from app.utils.panel_subscription_api import PanelSubscriptionApi


def get_user_repository(async_session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(async_session)


# auth
def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)


# user
async def get_current_user(token: str = Depends(oauth_scheme),
                           user_repository: UserRepository = Depends(get_user_repository)
                           ) -> UserSchema:
    token_data: TokenData = decode_access_token(token)
    user: UserSchema | None = await user_repository.get_by_tg_id(token_data.tg_id)
    if user is None:
        raise JwtCredentialsError("Could not validate credentials", {"WWW-Authenticate": "Bearer"})
    return user


async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)) -> UserSchema:
    if not current_user.is_active:
        raise IsActiveUserError("Inactive user")
    return current_user


# subscribe
def get_subscription_service_for_user(current_user: UserSchema = Depends(get_current_active_user)) -> SubscriptionService:
    sub_api = PanelSubscriptionApi(current_user.sub_uuid)
    return SubscriptionService(sub_api)


# panel
def get_panel_api() -> AsyncApi:
    return AsyncApi(settings.PANEL_HOST, settings.PANEL_USERNAME, settings.PANEL_PASSWORD,
                    use_tls_verify=settings.TLS_VERIFY)


def get_panel_service(panel_api: AsyncApi = Depends(get_panel_api)) -> PanelService:
    return PanelService(panel_api)


# payment
def get_payment_repository(async_session: AsyncSession = Depends(get_async_session)) -> PaymentRepository:
    return PaymentRepository(async_session)


def get_payment_service(
        payment_repository: PaymentRepository = Depends(get_payment_repository),
        user_repository: UserRepository = Depends(get_user_repository)
) -> PaymentService:
    return PaymentService(payment_repository, user_repository)
