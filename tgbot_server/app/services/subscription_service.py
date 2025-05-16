from app.repositories.interfaces import ISubscriptionRepository
from app.schema.subscription_schema import SubscriptionSchema


# class SubscriptionService:
#     def __init__(self, subscription_repository: ISubscriptionRepository):
#         self.repositories = subscription_repository
#
#     # async def user_subscriptions_from_server(self, user_id: int, server_id: int) -> list[SubscriptionSchema]:
#     #     return await self.repositories.get_all_from_server(user_id, server_id)
#
#     async def user_subscriptions_filtered_by_server(self, user_id: int) -> dict[str, list[SubscriptionSchema]]:
#         return await self.repositories.get_all_grouped(user_id)


class SubscriptionService:
    def __init__(
            self,
            subscription_repository: ISubscriptionRepository
    ):
        self.repository = subscription_repository

    async def create_subscription(
            self,
            user: UserSchema,
            server_id: int,
            subscription_data: SubscriptionCreate
    ) -> SubscriptionSchema:

        subscription = await self.repository.add(subscription_data)

        # try:
        #     await self.user_service.write_off_balance(user.id, subscription_data.price)
        #     await self.payment_service.create_subscription_payment(
        #         user.id,
        #         subscription_data.price,
        #         subscription_data.name
        #     )
        # except Exception as e:
        #     await self.repositories.delete(subscription.id)
        #     raise InternalServerError() from e

        return subscription

    async def user_subscriptions_filtered_by_server(self, user_id: int) -> dict[str, list[SubscriptionSchema]]:
        return await self.repository.get_all_grouped(user_id)
