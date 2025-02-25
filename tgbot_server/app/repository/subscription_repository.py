from datetime import datetime, UTC, timedelta
from itertools import groupby

from sqlalchemy import select, Result
from sqlalchemy.exc import NoResultFound, DatabaseError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import DBError, NotFoundError, DuplicatedError
from app.model import Subscription, Server
from app.repository.interfaces import ISubscriptionRepository
from app.schema.connect_schema import ConnectSchema
from app.schema.subscription_schema import SubscriptionCreate, SubscriptionSchema


class SubscriptionRepository(ISubscriptionRepository):
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def add(self, subscription_create: SubscriptionCreate) -> SubscriptionSchema:
        query: Subscription = Subscription(**subscription_create.model_dump())
        try:
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
        except IntegrityError as e:
            raise DuplicatedError(detail=str(e.orig))
        except DatabaseError:
            raise DBError(detail="Database error occurred.")
        return SubscriptionSchema.model_validate(query)

    async def get_by_id(self, id: int) -> SubscriptionSchema | None:
        ...

    async def get_all_grouped(self, user_id: int) -> dict[str, list[SubscriptionSchema]]:
        try:
            stmt = (
                select(Subscription)
                .join(Server)  # Join the Server table
                .options(selectinload(Subscription.server_rel))  # Load the server relationship
                .where(Subscription.user_id == user_id)
                .order_by(Server.name)  # Order by server name
            )

            # Execute the query
            result = await self.session.execute(stmt)
            subscriptions = result.scalars().all()

            grouped_subscriptions = {
                server_name: [SubscriptionSchema.model_validate(sub) for sub in group]
                for server_name, group in groupby(subscriptions, key=lambda sub: sub.server_rel.name)
            }
            return grouped_subscriptions

        except NoResultFound:
            raise NotFoundError(detail="Subscriptions not found.")

        except DatabaseError:
            raise DBError(detail="Database error occurred.")

    async def get_all_from_server(self, user_id: int, server_id: int) -> list[SubscriptionSchema]:
        try:
            stmt = select(Subscription).where(Subscription.user_id == user_id, Subscription.server_id == server_id)
            result: Result = await self.session.execute(stmt)
            subscriptions = result.scalars().all()
            return [SubscriptionSchema.model_validate(subscription) for subscription in subscriptions]
        except NoResultFound:
            return []

    async def update_subscription_by_connect(self, sub_id: int, connect: ConnectSchema) -> SubscriptionSchema:
        try:
            subscription: Subscription | None = await self.session.get(Subscription, sub_id)

            subscription.url = connect.connect_url
            subscription.end_date = datetime.now(UTC) + timedelta(seconds=connect.remaining_seconds)

            await self.session.commit()
            await self.session.refresh(subscription)

        except NoResultFound:
            raise NotFoundError(detail="Subscription not found.")
        except DatabaseError:
            raise DBError(detail="Database error occurred.")

        return SubscriptionSchema.model_validate(subscription)
