from fastapi import Depends
from py3xui import AsyncApi as PanelAsyncApi
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_session
from app.core.exceptions import JwtCredentialsError, IsActiveUserError
from app.core.security import oauth_scheme, decode_access_token
from app.repository.payment_repository import PaymentRepository
from app.repository.server_repository import ServerRepository
from app.repository.subscription_repository import SubscriptionRepository
from app.schema.auth_schema import TokenData
from app.schema.user_schema import UserSchema
from app.services.auth_service import AuthService
from app.repository.user_repository import UserRepository
from app.services.panel_service import PanelService
from app.services.payment_service import PaymentService
from app.services.server_service import ServerService
from app.services.subscription_service import SubscriptionService
from app.services.user_service import UserService
from app.utils.panel_subscription_api import PanelSubscriptionApi


# _________________________________________________________________________________________________________
# user
def get_user_repository(async_session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(async_session)


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


# _________________________________________________________________________________________________________
# auth
def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)


# _________________________________________________________________________________________________________
# subscription
def get_subscription_repository(async_session: AsyncSession = Depends(get_async_session)) -> SubscriptionRepository:
    return SubscriptionRepository(async_session)


def get_subscription_service(
        subscription_repository: SubscriptionRepository = Depends(get_subscription_repository),
) -> SubscriptionService:
    return SubscriptionService(subscription_repository)


# _________________________________________________________________________________________________________
# server
def get_server_repository(async_session: AsyncSession = Depends(get_async_session)) -> ServerRepository:
    return ServerRepository(async_session)


def get_server_service(server_repository: ServerRepository = Depends(get_server_repository)) -> ServerService:
    return ServerService(server_repository)


# _________________________________________________________________________________________________________
# payment
def get_payment_repository(async_session: AsyncSession = Depends(get_async_session)) -> PaymentRepository:
    return PaymentRepository(async_session)


def get_payment_service(
        payment_repository: PaymentRepository = Depends(get_payment_repository),
        user_service: UserService = Depends(get_user_service),
) -> PaymentService:
    return PaymentService(payment_repository, user_service)


# _________________________________________________________________________________________________________
# panel
def get_panel_api() -> PanelAsyncApi:
    return PanelAsyncApi(
        settings.PANEL_HOST,
        settings.PANEL_USERNAME,
        settings.PANEL_PASSWORD,
        use_tls_verify=settings.TLS_VERIFY
    )


def get_sub_api() -> PanelSubscriptionApi:
    return PanelSubscriptionApi(
        settings.SUBSCRIPTION_API_PORT,
        settings.SUBSCRIPTION_API_PATH,
        use_tls_verify=settings.TLS_VERIFY
    )


def get_panel_service(
        subscription_repository: SubscriptionRepository = Depends(get_subscription_repository),
        server_repository: ServerRepository = Depends(get_server_repository),
        user_service: UserService = Depends(get_user_service),
        payment_service: PaymentService = Depends(get_payment_service)
) -> PanelService:
    return PanelService(subscription_repository, server_repository, user_service, payment_service)

