from datetime import datetime, UTC, timedelta
from itertools import groupby

from sqlalchemy import select, Result, delete
from sqlalchemy.exc import NoResultFound, DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import DBError, NotFoundError, DuplicatedError
from app.model import Subscription, Server
from app.repository.interfaces import ISubscriptionRepository
from app.schema.connect_schema import ConnectSchema
from app.schema.subscription_schema import SubscriptionCreate, SubscriptionSchema, SubscriptionUpdate


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
            await self.session.rollback()
            raise DuplicatedError(detail=str(e.orig))
        except DatabaseError:
            await self.session.rollback()
            raise DBError(detail="Database error occurred.")

        return SubscriptionSchema.model_validate(query)

    async def get_by_id(self, id: int) -> SubscriptionSchema | None:
        try:
            result: Subscription | None = await self.session.get(Subscription, id)
            if result:
                return SubscriptionSchema.model_validate(result)
            return None
        except DatabaseError:
            await self.session.rollback()
            raise DBError(detail="Database error occurred.")

    async def get_by_email(self, email: str) -> SubscriptionSchema | None:
        try:
            stmt = select(Subscription).where(Subscription.email == email)
            result: Result = await self.session.execute(stmt)
            subscription = result.scalar().one_or_none()
        except NoResultFound:
            return None
        except DatabaseError:
            await self.session.rollback()
            raise DBError(detail="Database error occurred.")

        return SubscriptionSchema.model_validate(subscription)

    async def get_all_grouped(self, user_id: int) -> dict[str, list[SubscriptionSchema]]:
        try:
            stmt = (
                select(Subscription)
                .join(Server)
                .options(selectinload(Subscription.server_rel))
                .where(Subscription.user_id == user_id)
                .order_by(Server.name)
            )

            result = await self.session.execute(stmt)
            subscriptions = result.scalars().all()
        except NoResultFound:
            raise NotFoundError(detail="Subscriptions not found.")
        except DatabaseError:
            await self.session.rollback()
            raise DBError(detail="Database error occurred.")

        grouped_subscriptions = {
            server_name: [SubscriptionSchema.model_validate(sub) for sub in group]
            for server_name, group in groupby(subscriptions, key=lambda sub: sub.server_rel.name)
        }
        return grouped_subscriptions

    async def get_all_from_server(self, user_id: int, server_id: int) -> list[SubscriptionSchema]:
        try:
            stmt = select(Subscription).where(Subscription.user_id == user_id, Subscription.server_id == server_id)
            result: Result = await self.session.execute(stmt)
            subscriptions = result.scalars().all()
        except NoResultFound:
            return []

        return [SubscriptionSchema.model_validate(subscription) for subscription in subscriptions]

    async def update_subscription_by_connect(self, sub_id: int, connect: ConnectSchema) -> SubscriptionSchema:
        try:
            subscription: Subscription | None = await self.session.get(Subscription, sub_id, with_for_update=True)

            if subscription:
                print(f"I have been updated: {subscription.email}")
                subscription.url = connect.connect_url
                subscription.is_active = connect.active

                if connect.remaining_seconds:
                    subscription.end_date = datetime.now(UTC) + timedelta(seconds=connect.remaining_seconds)
                elif connect.remaining_seconds is None:
                    subscription.end_date = None

                await self.session.commit()
                await self.session.refresh(subscription)

        except NoResultFound:
            raise NotFoundError(detail="Subscription not found.")
        except DatabaseError:
            await self.session.rollback()
            raise DBError(detail="Database error occurred.")

        return SubscriptionSchema.model_validate(subscription)

    async def update(self, sub_id: int, update_info: SubscriptionUpdate) -> SubscriptionSchema:
        try:
            subscription: Subscription | None = await self.session.get(Subscription, sub_id, with_for_update=True)

            if update_info.end_date is not None:
                subscription.end_date = update_info.end_date

            if update_info.is_active is not None:
                subscription.is_active = update_info.is_active

            if subscription.end_date and subscription.end_date.astimezone(UTC) < datetime.now(UTC):
                subscription.is_active = False

            await self.session.commit()
            await self.session.refresh(subscription)

        except NoResultFound:
            raise NotFoundError(detail=f"Subscription with ID {sub_id} not found")
        except DatabaseError:
            await self.session.rollback()
            raise DBError(detail="Database error occurred.")

        return SubscriptionSchema.model_validate(subscription)

    async def delete(self, sub_id: int) -> bool:
        try:
            stmt = delete(Subscription).where(Subscription.id == sub_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except DatabaseError:
            await self.session.rollback()
            raise DBError(detail="Database error occurred.")
