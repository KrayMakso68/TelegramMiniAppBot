from app.repository.interfaces import ISubscriptionRepository
from app.schema.subscription_schema import SubscriptionSchema


class SubscriptionService:
    def __init__(self, subscription_repository: ISubscriptionRepository):
        self.repository = subscription_repository

    async def get_user_subscriptions_by_server(self, user_id: int) -> dict[str, list[SubscriptionSchema]]:
        return await self.repository.get_all_grouped(user_id)

