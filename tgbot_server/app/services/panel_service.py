import functools
import uuid

from datetime import datetime, timedelta, UTC

from httpx import HTTPStatusError
from py3xui import AsyncApi, Inbound
from fastapi import status, HTTPException

from app.core.config import settings
from app.repository.interfaces import ISubscriptionRepository, IServerRepository
from app.schema.connect_schema import ConnectSchema
from app.schema.panel_schema import ClientSchema, ClientCreate, ClientUpdate
from app.core.exceptions import NotFoundError, UnsupportedProtocolError, InsufficientBalanceError, InternalServerError, InvalidSubscriptionTypeError
from app.schema.server_schema import ServerSchema
from app.schema.subscription_schema import SubscriptionCreate, SubscriptionSchema, SubscriptionUpdate
from app.schema.user_schema import UserSchema
from app.services.payment_service import PaymentService
from app.services.user_service import UserService
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

    def __init__(
            self,
            subscription_repository: ISubscriptionRepository,
            server_repository: IServerRepository,
            user_service: UserService,
            payment_service: PaymentService
    ):
        self.subscription_repository = subscription_repository
        self.server_repository = server_repository
        self.user_service = user_service
        self.payment_service = payment_service

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
    async def add_client(
            self,
            server_id: int,
            new_client_info: ClientCreate,
            user: UserSchema,
            panel_api
    ) -> dict[str, str]:

        inbounds: list[Inbound] = await panel_api.inbound.get_list()
        current_inbound: Inbound | None = None
        for inbound in inbounds:
            if inbound.protocol == new_client_info.protocol:
                current_inbound = inbound
                break
        if current_inbound is None:
            raise UnsupportedProtocolError(detail=f"Server does not support the {new_client_info.protocol} protocol.")

        new_id = str(uuid.uuid4())
        new_email = f"{new_client_info.short_name}@@{new_id.replace('-', '_')}"
        expiry_date = datetime.now() + timedelta(days=30.44 * new_client_info.months)
        x_time = int(expiry_date.timestamp() * 1000)

        new_client = ClientSchema(
            email=new_email,
            enable=True,
            id=new_id,
            expiry_time=x_time,
            flow="xtls-rprx-vision",
            sub_id=user.sub_uuid,
        )

        if user.balance >= new_client_info.price:
            await panel_api.client.add(current_inbound.id, [new_client])

            server = await self.server_repository.get_by_id(server_id)
            if server is None:
                raise NotFoundError(detail="Server not found.")

            sub_api = self.get_sub_api(server)
            connects_data: list[ConnectSchema] = await sub_api.get_connects_for_user(user.sub_uuid)

            new_connect = None
            for connect in connects_data:
                if connect.email == new_email:
                    new_connect = connect
                    break

            subscription_create = SubscriptionCreate(
                name=new_client_info.short_name,
                email=new_email,
                url=new_connect.connect_url,
                user_id=user.id,
                server_id=server_id,
                end_date=expiry_date
            )

            new_subscription: SubscriptionSchema = await self.subscription_repository.add(subscription_create)

            if new_subscription:
                try:
                    await self.user_service.write_off_balance(user.id, new_client_info.price)
                except NotFoundError:
                    raise NotFoundError(detail="User for balance write-off not found.")

                await self.payment_service.create_subscription_payment(
                    user.id,
                    new_client_info.price,
                    new_client_info.short_name
                )
            else:
                raise InternalServerError(detail="Error adding subscription to server.")
        else:
            raise InsufficientBalanceError(detail="Insufficient balance in the user's account to make a purchase.")

        return {"status": "OK"}

    @ensure_panel_session_active
    async def update_client(
            self,
            server_id: int,
            update_client_info: ClientUpdate,
            user: UserSchema,
            panel_api
    ) -> dict[str, str]:

        subscription: SubscriptionSchema | None = await self.subscription_repository.get_by_id(update_client_info.id)
        if subscription is None:
            raise NotFoundError(detail="Subscription not found.")

        if subscription.end_date is None:
            raise InvalidSubscriptionTypeError(detail="Update is not available for premium subscriptions")

        client_uuid: str = subscription.email.split('@@')[1].replace("_", "-")

        new_end_date: datetime | None = None
        if subscription.end_date and subscription.end_date.replace(tzinfo=UTC) > datetime.now(UTC):
            new_end_date = subscription.end_date + timedelta(days=30.44 * update_client_info.months)
        else:
            new_end_date = datetime.now() + timedelta(days=30.44 * update_client_info.months)
        new_x_time = int(new_end_date.timestamp() * 1000)

        client: ClientSchema = await self.get_client_info_by_email(server_id, subscription.email)
        client.enable = True
        client.expiry_time = new_x_time
        client.id = client_uuid
        client.flow = 'xtls-rprx-vision'
        client.sub_id = user.sub_uuid
        client.limit_ip = 1

        if user.balance >= update_client_info.price:
            await panel_api.client.update(client_uuid, client)

            update_data = SubscriptionUpdate(
                end_date=new_end_date,
                is_active=True
            )

            await self.subscription_repository.update(update_client_info.id, update_data)

            try:
                await self.user_service.write_off_balance(user.id, update_client_info.price)
            except NotFoundError:
                raise NotFoundError(detail="User for balance write-off not found.")

            await self.payment_service.create_subscription_payment(
                user.id,
                update_client_info.price,
                subscription.name
            )
        else:
            raise InsufficientBalanceError(detail="Insufficient balance in the user's account to make a purchase.")

        return {"status": "OK"}

    async def update_user_subscriptions_from_server(
            self, user: UserSchema,
            server_id: int | None = None,
            all_servers: bool = False
    ) -> dict[str, str]:

        servers_list: list[ServerSchema] = []
        if all_servers:
            servers_list = await self.server_repository.get_all()
            if len(servers_list) == 0:
                raise NotFoundError(detail="Servers for update not found.")
        elif server_id:
            server = await self.server_repository.get_by_id(server_id)
            if server is None:
                raise NotFoundError(detail="Server not found.")
            else:
                servers_list = [server]

        for server in servers_list:
            sub_api = self.get_sub_api(server)
            try:
                connects_data: list[ConnectSchema] = await sub_api.get_connects_for_user(user.sub_uuid)
            except Exception:
                print(f"Error retrieving subscription data from server: {server.name}")
                continue

            existing_subscriptions = await self.subscription_repository.get_all_from_server(user.id, server.id)
            existing_subscriptions_dict = {sub.email: sub for sub in existing_subscriptions}

            server_emails = {connect.email for connect in connects_data}

            for connect_data in connects_data:
                if connect_data.email in existing_subscriptions_dict:
                    existing_sub = existing_subscriptions_dict[connect_data.email]

                    if not self.compare_connect_subscription(connect_data, existing_sub):
                        await self.subscription_repository.update_subscription_by_connect(existing_sub.id, connect_data)
                else:
                    new_subscription = SubscriptionCreate(
                        email=connect_data.email,
                        name=connect_data.name,
                        url=connect_data.connect_url,
                        user_id=user.id,
                        server_id=server.id,
                        is_active=connect_data.active
                    )
                    if connect_data.remaining_seconds:
                        new_subscription.end_date = datetime.now(UTC) + timedelta(
                            seconds=connect_data.remaining_seconds)
                    elif not connect_data.active:
                        new_subscription.end_date = datetime.now(UTC) - timedelta(days=1)

                    await self.subscription_repository.add(new_subscription)

            for existing_sub in existing_subscriptions:
                if existing_sub.email not in server_emails:
                    await self.subscription_repository.delete(existing_sub.id)
                    print(f"Deleted subscription {existing_sub.email} as it no longer exists on server")

        return {"status": "OK"}

    @staticmethod
    def compare_connect_subscription(
            connect: ConnectSchema,
            sub: SubscriptionSchema,
            time_tolerance: timedelta = timedelta(minutes=30)
    ) -> bool:

        if not all([
            connect.email == sub.email,
            connect.name == sub.name,
            connect.active == sub.is_active
        ]):
            return False

        if connect.remaining_seconds is not None:
            if connect.remaining_seconds == 0:
                return not sub.is_active
            else:
                if sub.end_date is not None:
                    sub_remaining_seconds = int((sub.end_date - datetime.now(UTC)).total_seconds())
                else:
                    sub_remaining_seconds = 0
                return abs(connect.remaining_seconds - sub_remaining_seconds) <= time_tolerance.total_seconds()
        else:
            return sub.end_date is None

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
