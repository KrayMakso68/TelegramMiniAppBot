import asyncio
import logging
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database import get_db

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.is_running = True

    async def start(self):
        logger.info("Запуск планировщика")
        while self.is_running:
            try:
                async for session in get_db():
                    await self._run_checks(session)
            except Exception as e:
                logger.error(f"Ошибка в планировщике: {e}", exc_info=True)
            finally:
                await asyncio.sleep(12 * 3600)  # 12 часов

    async def _run_checks(self, session: AsyncSession):
        from bot.services.reminders import SubscriptionChecker

        checker = SubscriptionChecker(self.bot, session)
        await checker.check_all_subscriptions()

    async def stop(self):
        self.is_running = False
        logger.info("Планировщик остановлен")
