from app.core.exceptions import NotFoundError
from app.repository.interfaces import IUserRepository
from app.core.config import settings
from app.utils.telegram_api import TelegramApi


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def get_user_avatar(self, user_tg_id: int) -> str:
        tg_api = TelegramApi(settings.BOT_TOKEN)
        return await tg_api.get_user_avatar(user_tg_id)

    async def top_up_balance(self, user_id: int, amount: float) -> float:
        user_current_balance = await self.user_repository.get_user_balance(user_id)
        if user_current_balance is not None:
            new_balance = user_current_balance + amount
            await self.user_repository.update_balance(user_id, new_balance)
            return new_balance
        else:
            raise NotFoundError(detail="User not found.")

    async def write_off_balance(self, user_id: int, amount: float) -> float:
        user_current_balance = await self.user_repository.get_user_balance(user_id)
        if user_current_balance is not None:
            new_balance = user_current_balance - amount
            await self.user_repository.update_balance(user_id, new_balance)
            return new_balance
        else:
            raise NotFoundError(detail="User not found.")