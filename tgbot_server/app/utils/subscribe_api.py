from fastapi import HTTPException, status
from httpx import AsyncClient, HTTPError

from app.core.config import settings
from app.schema.subscribe_schema import VlessConfig


class SubscribeApi:
    def __init__(self, sub_uuid):
        self.sub_uuid = sub_uuid
        self.sub_base_url = settings.SUBSCRIBE_API_URL

    async def get_subscribes(self) -> list[VlessConfig]:
        url = self.sub_base_url + self.sub_uuid

        async with AsyncClient(verify=False) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.text.splitlines()
                return [VlessConfig.from_url(config) for config in data]
            except HTTPError:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found.")
