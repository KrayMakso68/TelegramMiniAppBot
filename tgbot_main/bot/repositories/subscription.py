import logging

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bot.models.subscription import Subscription
from bot.schemas.subscription import SubscriptionSchema


logger = logging.getLogger(__name__)


class SubscriptionRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_without_premium(self) -> [SubscriptionSchema]:
        try:
            result = await self.session.execute(
                select(Subscription)
                .where(Subscription.is_active == True)
                .where(Subscription.end_date != None)
                .options(
                    joinedload(Subscription.user_rel)
                )
            )
            subscriptions = result.unique().scalars().all()

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении активных подписок: {e}")
            raise RepositoryError("Не удалось получить активные подписки") from e

        return [SubscriptionSchema.model_validate(subscription) for subscription in subscriptions]

    async def save(self, subscription_schema: SubscriptionSchema) -> None:
        subscription: Subscription = Subscription(**subscription_schema.model_dump())
        try:
            self.session.add(subscription)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка сохранения подписки {subscription.id}: {e}")
            raise RepositoryError("Не удалось сохранить подписку") from e

    async def update(self, sub_id: int, update_data: dict) -> bool:
        """Обновление любых полей подписки"""
        try:
            result = await self.session.execute(
                update(Subscription)
                .where(Subscription.id == sub_id)
                .values(**update_data)
            )
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка обновления подписки {sub_id}: {e}")
            raise RepositoryError("Не удалось обновить подписку") from e


class RepositoryError(Exception):
    """Кастомное исключение для ошибок репозитория"""
    pass