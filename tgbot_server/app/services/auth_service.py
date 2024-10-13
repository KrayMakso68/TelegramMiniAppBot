from app.core.security import create_access_token
from app.utils.validate_telegram import get_webapp_data
from app.repository.interfaces import IUserRepository
from app.schema.auth_schema import WebAppInitData, TokenInfo, InitAuthData
from app.schema.user_schema import UserSchema, UserCreate


class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def login(self, login_info: InitAuthData) -> TokenInfo:
        webapp_data: WebAppInitData = get_webapp_data(login_info)
        user: UserSchema | None = await self.user_repository.get_by_tg_id(webapp_data.user.id)
        if not user:
            user_create = UserCreate(tg_id=webapp_data.user.id)
            user: UserSchema = await self.user_repository.add(user_create)

        payload = {"tg_id": user.tg_id}
        access_token = create_access_token(data=payload)
        return TokenInfo(
            access_token=access_token,
            token_type="bearer"
        )
