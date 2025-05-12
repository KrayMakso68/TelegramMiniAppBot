import logging
from datetime import datetime, timedelta, timezone
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import config
from bot.repositories.subscription import SubscriptionRepo
from bot.schemas.subscription import SubscriptionSchema

logger = logging.getLogger(__name__)


class SubscriptionChecker:
    def __init__(self, bot: Bot, session: AsyncSession):
        self.bot = bot
        self.repo = SubscriptionRepo(session)

    async def check_all_subscriptions(self):
        try:
            logger.info("Запуск проверки подписок")
            active_subs: [SubscriptionSchema] = await self.repo.get_active_without_premium()

            for sub in active_subs:
                await self._process_single_subscription(sub)

            logger.info(f"Проверено {len(active_subs)} подписок")

        except Exception as e:
            logger.error(f"Ошибка при проверке подписок: {e}", exc_info=True)

    async def _process_single_subscription(self, sub: SubscriptionSchema):
        try:
            if not sub.end_date:
                return

            now = datetime.now(timezone.utc)
            remaining = sub.end_date - now

            if remaining <= timedelta(0):
                await self._handle_expired_subscription(sub)
            else:
                await self._check_reminders(sub, remaining)

        except Exception as e:
            logger.error(f"Ошибка обработки подписки {sub.id}: {e}", exc_info=True)

    async def _check_reminders(self, sub: SubscriptionSchema, remaining: timedelta):
        if remaining <= timedelta(days=3) and not sub.notified_3_days:
            await self._send_notification(sub, days_left=3)
            await self._update_notification_status(sub, days=3)

        elif remaining <= timedelta(days=1) and not sub.notified_1_day:
            await self._send_notification(sub, days_left=1)
            await self._update_notification_status(sub, days=1)

    async def _handle_expired_subscription(self, sub: SubscriptionSchema):
        if sub.is_active:
            await self._send_expired_notification(sub)
            await self.repo.update(sub.id, {"is_active": False})

    async def _send_notification(self, sub: SubscriptionSchema, days_left: int):
        try:
            message = self._build_reminder_message(sub, days_left)
            await self.bot.send_message(
                chat_id=sub.user_rel.tg_id,
                text=message,
                parse_mode="HTML",
                reply_markup=self._get_markup()
            )
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление для {sub.user_id}: {e}")

    async def _send_expired_notification(self, sub: SubscriptionSchema):
        try:
            message = self._build_expired_message(sub)
            await self.bot.send_message(
                chat_id=sub.user_rel.tg_id,
                text=message,
                parse_mode="HTML",
                reply_markup=self._get_markup()
            )
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление об истечении для {sub.user_id}: {e}")

    def _build_reminder_message(self, sub: SubscriptionSchema, days_left: int) -> str:
        return (
            "🔔 <b><u>УВЕДОМЛЕНИЕ</u></b> 🔔\n\n"

            f"⚡️ <i>Подключение:  </i> <code>{sub.name}</code> ⚡️\n\n"

            "🕒 <b>Истекает через:</b> \n"
            "┏━━━━━━━━━━━━━┓\n"
            f"              <b>{days_left} {self._days_text(days_left)}!</b> 🚨\n"
            "┗━━━━━━━━━━━━━┛\n\n"

            "🔄 <u>Продлите сейчас</u>"
        )

    def _build_expired_message(self, sub: SubscriptionSchema) -> str:
        return (
            "🔔 <b><u>СРОЧНОЕ УВЕДОМЛЕНИЕ</u></b> 🔔\n\n"

            f"⚡ <i>Подключение:</i> <code>{sub.name}</code> ⚡\n\n"

            "🕒 <b>Статус подписки:</b>\n"
            "┏━━━━━━━━━━━━━┓\n"
            "              <b>ИСТЕКЛО</b> 🚫\n"
            "┗━━━━━━━━━━━━━┛\n\n"

            "⚠️ <b>Доступ приостановлен!</b>\n"
            "🔄 <u>Продлите сейчас</u> "
        )

    async def _update_notification_status(self, sub: SubscriptionSchema, days: int):
        update_data = {
            3: {"notified_3_days": True},
            1: {"notified_1_day": True}
        }
        await self.repo.update(sub.id, update_data[days])

    @staticmethod
    def _days_text(days: int) -> str:

        last_digit = days % 10
        if last_digit == 1 and days != 11:
            return "день"
        elif 2 <= last_digit <= 4 and days not in (12, 13, 14):
            return "дня"
        return "дней"

    @staticmethod
    def _get_markup():
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Продлить подписку ⏳",
                        web_app=WebAppInfo(url=config.WEBAPP_URL),
                    )
                ]
            ]
        )
        return markup
