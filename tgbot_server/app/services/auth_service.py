from datetime import timedelta

from app.core.security import create_access_token
from app.utils.validate_telegram import check_webapp_signature
from app.core.config import configs
from app.repository.interfaces import IUserRepository
from app.schema.auth_schema import WebAppInitData, Token
from app.schema.user_schema import UserSchema, UserCreate


class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def login(self, login_info: WebAppInitData) -> Token:
        if check_webapp_signature(configs.BOT_TOKEN, login_info):

            user: UserSchema | None = await self.user_repository.get_by_tg_id(login_info.user.id)
            if not user:
                user_create = UserCreate(tg_id=login_info.user.id)
                user: UserSchema = await self.user_repository.add(user_create)

            access_token_expires = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"tg_id": user.tg_id}, expires_delta=access_token_expires
            )
            return Token(access_token=access_token, token_type="bearer")
