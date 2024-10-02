from app.model.user_model import User
from app.repository.user_repository import UserRepository
from app.schema.auth_schema import WebAppInitData
from app.schema.user_schema import User
from app.services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def login(self, login_info: WebAppInitData):
        user: User = await self.user_repository.read_by_tg_id(WebAppInitData.user.id)
        if not user:
            user_schema = User(

            )
            await self.user_repository.create()

