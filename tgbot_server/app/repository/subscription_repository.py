from itertools import groupby

from sqlalchemy import select, Result
from sqlalchemy.exc import NoResultFound, DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import DBError, NotFoundError
from app.model import Subscription, Server
from app.repository.interfaces import ISubscriptionRepository
from app.schema.subscription_schema import SubscriptionCreate, SubscriptionSchema


class SubscriptionRepository(ISubscriptionRepository):
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def add(self, subscription_create: SubscriptionCreate) -> SubscriptionSchema:
        ...

    async def get_by_id(self, id: int) -> SubscriptionSchema | None:
        ...

    async def get_all_grouped(self, user_id: int) -> dict[str, list[SubscriptionSchema]]:
        try:
            result = await self.session.execute(
                select(Subscription)
                .options(selectinload(Subscription.server_rel))
                .filter(Subscription.user_id == user_id)
                .order_by(Server.name)
            )
            subscriptions = result.scalars().all()
            grouped_subscriptions = {
                server_name: [SubscriptionSchema.model_validate(sub) for sub in group]
                for server_name, group in groupby(subscriptions, key=lambda sub: sub.server.name)
            }
            return grouped_subscriptions

        except NoResultFound:
            raise NotFoundError(detail="Subscriptions not found.")

        except DatabaseError:
            raise DBError(detail="Database error occurred.")
