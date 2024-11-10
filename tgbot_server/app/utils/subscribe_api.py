from fastapi import HTTPException, status
from httpx import AsyncClient, HTTPError

from app.core.config import settings
from app.schema.subscribe_schema import VlessConfig, ConnectSchema


class SubscribeApi:
    def __init__(self, sub_uuid):
        self.url = settings.SUBSCRIBE_API_URL + sub_uuid
        self.timeout = 30

    async def get_subscribe_configs(self) -> list[VlessConfig]:
        async with AsyncClient(verify=settings.TLS_VERIFY) as client:
            try:
                response = await client.get(self.url, timeout=self.timeout)
                response.raise_for_status()
                data = response.text.splitlines()
                return [VlessConfig.from_url(config) for config in data]
            except HTTPError:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found.")

    async def get_subscribe_connects(self) -> list[ConnectSchema]:
        async with AsyncClient(verify=settings.TLS_VERIFY) as client:
            try:
                response = await client.get(self.url, timeout=self.timeout)
                response.raise_for_status()
                data = response.text.splitlines()
                return [ConnectSchema.from_url(config) for config in data]
            except HTTPError:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found.")
