from httpx import AsyncClient, HTTPError, RequestError, TimeoutException

from app.core.exceptions import NotFoundError, InternalServerError, ServiceUnavailableError
from app.schema.connect_schema import ConnectSchema


class PanelSubscriptionApi:

    def __init__(self, subscription_url: str, use_tls_verify: bool = True):
        self.subscription_url = subscription_url
        self.use_tls_verify = use_tls_verify
        self.timeout = 30

    async def get_connects_for_user(self, user_sub_uuid: str) -> list[ConnectSchema]:
        url = self._create_user_url(user_sub_uuid)

        async with AsyncClient(verify=self.use_tls_verify) as client:
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

    def _create_user_url(self, user_sub_uuid: str) -> str:
        return self.subscription_url + user_sub_uuid
