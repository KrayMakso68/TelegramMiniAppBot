from py3xui import AsyncApi, Client

from app.core.config import settings


class PanelService:
    def __init__(self):
        self.panel_api = AsyncApi(settings.XUI_HOST, settings.XUI_USERNAME, settings.XUI_PASSWORD)

    async def get_client_info_by_id(self, client_uuid) -> list[Client]:
        return await self.panel_api.client.get_traffic_by_id(client_uuid)

    async def get_client_info_by_email(self, client_email) -> Client:
        return await self.panel_api.client.get_by_email(client_email)

    async def add_client(self):
        return ...
