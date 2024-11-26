from httpx import AsyncClient, HTTPError, RequestError, TimeoutException

from app.core.config import settings
from app.core.exceptions import NotFoundError, InternalServerError, ServiceUnavailableError
from app.schema.subscribe_schema import VlessConfig, ConnectSchema


class SubscribeApi:
    def __init__(self, sub_uuid):
        self.url = settings.SUBSCRIBE_API_URL + sub_uuid
        self.timeout = 30

    async def get_subscribe_configs(self) -> list[VlessConfig]:
        async with AsyncClient(verify=settings.TLS_VERIFY) as client:
            try:
                response = await client.get(self.url, timeout=self.timeout)

                if response.status_code == 400:
                    raise NotFoundError(detail="Configs not found.")

                response.raise_for_status()
                data = response.text.splitlines()
                return [VlessConfig.from_url(config) for config in data]

            except HTTPError:
                raise InternalServerError(detail="Server error.")

            except (RequestError, TimeoutException):
                raise ServiceUnavailableError(detail="Connection error.")

    async def get_subscribe_connects(self) -> list[ConnectSchema]:
        async with AsyncClient(verify=settings.TLS_VERIFY) as client:
            try:
                response = await client.get(self.url, timeout=self.timeout)

                if response.status_code == 400:
                    raise NotFoundError(detail="Connects not found.")

                response.raise_for_status()
                data = response.text.splitlines()
                return [ConnectSchema.from_url(config) for config in data]

            except HTTPError:
                raise InternalServerError(detail="Server error.")

            except (RequestError, TimeoutException):
                raise ServiceUnavailableError(detail="Connection error.")
