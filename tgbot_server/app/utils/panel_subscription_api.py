from httpx import AsyncClient, HTTPError, RequestError, TimeoutException

from app.core.config import settings
from app.core.exceptions import NotFoundError, InternalServerError, ServiceUnavailableError
from app.schema.connect_schema import ConnectSchema


class PanelSubscriptionApi:
    def __init__(self, sub_uuid: str):
    # def __init__(self, user_id: int, sub_uuid: str):
        self.url = settings.SUBSCRIPTION_API_URL + sub_uuid
        # self.user_id = user_id
        # self.sub_uuid = sub_uuid
        self.timeout = 30

    async def get_connects(self) -> list[ConnectSchema]:
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

    # async def get_connects_from_server(self, server_ip) -> list[ConnectSchema]:
    #     async with AsyncClient(verify=settings.TLS_VERIFY) as client:
    #         try:
    #             response = await client.get(f'https://{server_ip}:61802/sub-61eeb58a-a9f2-4ae9-8959-7ef1e751ec52/{self.sub_uuid}', timeout=self.timeout)
    #
    #             if response.status_code == 400:
    #                 raise NotFoundError(detail="Connects not found.")
    #
    #             response.raise_for_status()
    #             data = response.text.splitlines()
    #             return [ConnectSchema.from_url(config) for config in data]
    #
    #         except HTTPError:
    #             raise InternalServerError(detail="Server error.")
    #
    #         except (RequestError, TimeoutException):
    #             raise ServiceUnavailableError(detail="Connection error.")