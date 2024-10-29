from app.repository.interfaces import IUserRepository
from app.core.config import settings
from app.utils.telegram_api import TelegramApi


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def get_user_avatar(self, user_tg_id: int) -> str:
        telegram_api = TelegramApi(settings.BOT_TOKEN)
        return await telegram_api.get_user_avatar(user_tg_id)
