from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.interfaces import ISubscriptionRepository
from app.schema.subscription_schema import SubscriptionCreate, SubscriptionSchema


class SubscriptionRepository(ISubscriptionRepository):
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def add(self, subscription_create: SubscriptionCreate) -> SubscriptionSchema:
        ...

    async def get_by_id(self, id: int) -> SubscriptionSchema | None:
        ...
    