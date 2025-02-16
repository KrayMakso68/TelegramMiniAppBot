import functools
import uuid

from httpx import HTTPStatusError
from py3xui import AsyncApi
from fastapi import status, HTTPException

from app.schema.panel_schema import ClientSchema, ClientCreate
from app.core.exceptions import NotFoundError
from app.schema.user_schema import UserSchema
from app.utils.panel_subscription_api import PanelSubscriptionApi


def ensure_panel_session_active(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):

        if not self.panel_api.session:
            await self.panel_api.login()

        try:
            response = await method(self, *args, **kwargs)
            return response
        except HTTPStatusError as e:
            if e.response.status_code == status.HTTP_307_TEMPORARY_REDIRECT:
                await self.panel_api.login()
                response = await method(self, *args, **kwargs)
                return response
            raise HTTPException(e.response.status_code, detail=e.response.text)

    return wrapper


class PanelService:
    def __init__(self, panel_api: AsyncApi, sub_api: PanelSubscriptionApi):
        self.panel_api = panel_api
        self.sub_api = sub_api

    @ensure_panel_session_active
    async def get_client_info_by_id(self, client_uuid: str) -> list[ClientSchema]:
        response: list[ClientSchema] = await self.panel_api.client.get_traffic_by_id(client_uuid)
        if len(response) == 0:
            raise NotFoundError(detail="Client Not Found.")
        return response

    @ensure_panel_session_active
    async def get_client_info_by_email(self, client_email: str) -> ClientSchema:
        response: ClientSchema | None = await self.panel_api.client.get_by_email(client_email)
        if response is None:
            raise NotFoundError(detail="Client Not Found.")
        return response

    @ensure_panel_session_active
    async def add_clients(self, add_list: list[ClientCreate], user: UserSchema):
        for client in add_list:
            new_client = ClientSchema(
                email=client.email + uuid.uuid4(),
                enable=True,
                id=str(uuid.uuid4()),
                expiry_time=28174912,
                flow="xtls-rprx-vision",
                sub_id=user.sub_uuid,
                tg_id=user.tg_id

            )
        new_clients: list[ClientSchema] = []
        new_client = ClientSchema(
            id=str(uuid.uuid4()),
            email="test",
            enable=True
        )
        return

    

# import uuid
#             api = py3xui.AsyncApi.from_env()
#             await api.login()
#
#             new_client = py3xui.Client(id=str(uuid.uuid4()), email="test", enable=True)
#             inbound_id = 1
#
#             await api.client.add(inbound_id, [new_client])