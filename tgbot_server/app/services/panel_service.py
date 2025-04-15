import functools
import uuid

from datetime import datetime, timedelta, UTC

from httpx import HTTPStatusError
from py3xui import AsyncApi, Inbound
from fastapi import status, HTTPException

from app.core.config import settings
from app.repository import subscription_repository
from app.repository.interfaces import ISubscriptionRepository, IServerRepository
from app.schema.connect_schema import ConnectSchema
from app.schema.panel_schema import ClientSchema, ClientCreate
from app.core.exceptions import NotFoundError, UnsupportedProtocolError
from app.schema.server_schema import ServerSchema
from app.schema.subscription_schema import SubscriptionCreate
from app.schema.user_schema import UserSchema
from app.utils.panel_subscription_api import PanelSubscriptionApi


def ensure_panel_session_active(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        server_id = kwargs.get("server_id") or (args[0] if args else None)
        if server_id is None:
            raise HTTPException(status_code=400, detail="server_id is require")

        server = await self.server_repository.get_by_id(server_id)
        if server is None:
            raise NotFoundError(detail="Server Not Found.")

        if server_id in self._panel_sessions:
            panel_api = self._panel_sessions[server_id]
        else:
            panel_api = self.get_panel_api(server)
            self._panel_sessions[server_id] = panel_api

        if not panel_api.session:
            await panel_api.login()

        try:
            return await method(self, panel_api=panel_api, *args, **kwargs)
        except HTTPStatusError as e:
            if e.response.status_code == status.HTTP_307_TEMPORARY_REDIRECT:
                await panel_api.login()
                return await method(self, panel_api=panel_api, *args, **kwargs)
            raise HTTPException(e.response.status_code, detail=e.response.text)

    return wrapper


class PanelService:
    _panel_sessions = {}

    def __init__(self, subscription_repository: ISubscriptionRepository, server_repository: IServerRepository):
        self.subscription_repository = subscription_repository
        self.server_repository = server_repository

    @ensure_panel_session_active
    async def get_client_info_by_id(self, server_id: int, client_uuid: str, panel_api) -> list[ClientSchema]:
        response: list[ClientSchema] = await panel_api.client.get_traffic_by_id(client_uuid)

        if len(response) == 0:
            raise NotFoundError(detail="Client Not Found.")

        return response

    @ensure_panel_session_active
    async def get_client_info_by_email(self, server_id: int, client_email: str, panel_api) -> ClientSchema:
        response: ClientSchema | None = await panel_api.client.get_by_email(client_email)

        if response is None:
            raise NotFoundError(detail="Client Not Found.")

        return response

    @ensure_panel_session_active
    async def add_client(self, server_id: int, new_client_info: ClientCreate, user: UserSchema, panel_api):

        inbounds: list[Inbound] = panel_api.inbound.get_list()
        current_inbound: Inbound | None = None
        for inbound in inbounds:
            if inbound.protocol == new_client_info.protocol:
                current_inbound = inbound
                break
        if current_inbound is None:
            raise UnsupportedProtocolError(detail=f"Server does not support the {new_client_info.protocol} protocol.")
        new_id = str(uuid.uuid4())
        expiry_time = int(timedelta(days=30 * new_client_info.months).total_seconds())

        new_client = ClientSchema(
            email=f"{new_client_info.short_name}@{new_id}",
            enable=True,
            id=new_id,
            expiry_time=expiry_time,
            flow="xtls-rprx-vision",
            sub_id=user.sub_uuid,
            tg_id=user.tg_id
        )



        # for client in add_list:
        #     new_client = ClientSchema(
        #         email=client.email + uuid.uuid4(),
        #         enable=True,
        #         id=str(uuid.uuid4()),
        #         expiry_time=28174912,
        #         flow="xtls-rprx-vision",
        #         sub_id=user.sub_uuid,
        #         tg_id=user.tg_id
        #     )
        # new_clients: list[ClientSchema] = []
        # new_client = ClientSchema(
        #     id=str(uuid.uuid4()),
        #     email="test",
        #     enable=True
        # )
        return

    # async def get_user_subscriptions_from_server(self, sub_uuid: str, server_id: int) -> list[ConnectSchema]:
    #     server = await self.server_repository.get_by_id(server_id)
    #     if server is None:
    #         raise NotFoundError(detail="Server Not Found.")
    #
    #     sub_api = self.get_sub_api(server)
    #
    #     return await sub_api.get_connects_for_user(sub_uuid)

    async def update_user_subscriptions(self, user: UserSchema):
        servers: list[ServerSchema] = await self.server_repository.get_all()

        for server in servers:
            sub_api = self.get_sub_api(server)
            try:
                connects_data: list[ConnectSchema] = await sub_api.get_connects_for_user(user.sub_uuid)
            except Exception as e:
                print(f"Ошибка получения данных подписки с сервера {server.name}")
                continue

            existing_subscriptions = await self.subscription_repository.get_all_from_server(user.id, server.id)
            existing_subscriptions_dict = {sub.email_name: sub for sub in existing_subscriptions}

            for connect_data in connects_data:
                connect_schema = ConnectSchema.model_validate(connect_data)

                if connect_schema.email in existing_subscriptions_dict:
                    existing_sub = existing_subscriptions_dict[connect_schema.email]

                    await self.subscription_repository.update_subscription_by_connect(existing_sub.id, connect_schema)
                else:
                    new_subscription = SubscriptionCreate(
                        email_name=connect_schema.email,
                        url=connect_schema.connect_url,
                        user_id=user.id,
                        server_id=server.id,
                        is_active=connect_schema.active
                    )
                    if connect_schema.remaining_seconds:
                        new_subscription.end_date = datetime.now(UTC) + timedelta(
                            seconds=connect_schema.remaining_seconds)
                    elif not connect_schema.active:
                        new_subscription.end_date = datetime.now(UTC) - timedelta(days=1)

                    await self.subscription_repository.add(new_subscription)
        return await self.subscription_repository.get_all_grouped(user.id)

    @staticmethod
    def get_panel_api(server: ServerSchema) -> AsyncApi:
        return AsyncApi(
            server.panel_url,
            server.username,
            server.password_enc,
            use_tls_verify=settings.TLS_VERIFY
        )

    @staticmethod
    def get_sub_api(server: ServerSchema) -> PanelSubscriptionApi:
        return PanelSubscriptionApi(
            server.subscription_url,
            use_tls_verify=settings.TLS_VERIFY
        )

# import uuid
#             api = py3xui.AsyncApi.from_env()
#             await api.login()
#
#             new_client = py3xui.Client(id=str(uuid.uuid4()), email="test", enable=True)
#             inbound_id = 1
#
#             await api.client.add(inbound_id, [new_client])
