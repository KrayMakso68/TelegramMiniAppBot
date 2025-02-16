from httpx import AsyncClient, HTTPError, RequestError, TimeoutException

from app.core.config import settings
from app.core.exceptions import NotFoundError, InternalServerError, ServiceUnavailableError
from app.schema.connect_schema import ConnectSchema


class PanelSubscriptionApi:

    def __init__(self, port: str, path: str):
        self.port = port
        self.path = path
        self.timeout = 30

    async def get_connects_from_server(self, server_ip: str, user_sub_uuid: str) -> list[ConnectSchema]:
        url = self._create_url(server_ip, user_sub_uuid)

        async with AsyncClient(verify=settings.TLS_VERIFY) as client:
            try:
                response = await client.get(url, timeout=self.timeout)

                if response.status_code == 400:
                    raise NotFoundError(detail="Connects not found.")

                response.raise_for_status()
                data = response.text.splitlines()
                return [ConnectSchema.from_url(config) for config in data]

            except HTTPError:
                raise InternalServerError(detail="Server error.")

            except (RequestError, TimeoutException):
                raise ServiceUnavailableError(detail="Connection error.")

    def _create_url(self, server_ip: str, user_sub_uuid: str) -> str:
        return f'https://{server_ip}:{self.port}/{self.path}/{user_sub_uuid}'
