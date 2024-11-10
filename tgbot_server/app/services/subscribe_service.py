from app.schema.subscribe_schema import VlessConfig, ConnectSchema
from app.utils.subscribe_api import SubscribeApi


class SubscribeService:
    def __init__(self, sub_api: SubscribeApi):
        self.api = sub_api

    async def get_user_configs(self) -> list[VlessConfig]:
        return await self.api.get_subscribe_configs()

    async def get_user_connects(self) -> list[ConnectSchema]:
        return await self.api.get_subscribe_connects()
