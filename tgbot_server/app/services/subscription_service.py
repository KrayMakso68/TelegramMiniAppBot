from app.schema.connect_schema import ConnectSchema
from app.utils.panel_subscription_api import PanelSubscriptionApi


class SubscriptionService:
    def __init__(self, sub_api: PanelSubscriptionApi):
        self.api = sub_api

    async def get_user_connects(self) -> list[ConnectSchema]:
        return await self.api.get_connects()

