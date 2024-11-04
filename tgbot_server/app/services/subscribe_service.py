from typing import Any

from app.utils.subscribe_api import SubscribeApi


class SubscribeService:
    def __init__(self, sub_api: SubscribeApi):
        self.api = sub_api

    async def get_user_subscribes(self) -> list[Any]:
        return await self.api.get_subscribes()
