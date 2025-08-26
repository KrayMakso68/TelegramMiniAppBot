from fastapi import APIRouter, Depends

from app.api.dependencies import get_panel_service, get_current_active_user, get_subscription_service
from app.schema.connect_schema import ConnectSchema
from app.schema.panel_schema import ClientSchema, ClientCreateRequest, ClientUpdateRequest, ClientDeleteRequest, \
    ClientCreateDTO, ClientUpdateDTO, ClientDeleteDTO
from app.schema.user_schema import UserSchema
from app.services.panel_service import PanelService
from app.services.subscription_service import SubscriptionService

router = APIRouter(
    prefix="/panel",
    tags=["panel"]
)


@router.get("/{server_id}/client/info-by-uuid/{client_uuid}")
async def get_clients_by_uuid(
        server_id: int,
        client_uuid: str,
        service: PanelService = Depends(get_panel_service)
) -> list[ClientSchema]:
    return await service.get_client_info_by_id(server_id, client_uuid)


@router.get("/{server_id}/client/info-by-email/{client_email}")
async def get_client_by_email(
        server_id: int,
        client_email: str,
        service: PanelService = Depends(get_panel_service)
) -> ClientSchema:
    return await service.get_client_info_by_email(server_id, client_email)


@router.post("/subscription/update-all")
async def update_clients(
        user: UserSchema = Depends(get_current_active_user),
        service: PanelService = Depends(get_panel_service)
) -> dict[str, str]:
    return await service.update_user_subscriptions_from_server(user, all_servers=True)


@router.post("/{server_id}/client/add")
async def add_client_and_check(
        server_id: int,
        new_client_info: ClientCreateRequest,
        user: UserSchema = Depends(get_current_active_user),
        service: PanelService = Depends(get_panel_service)
) -> dict[str, str]:

    data = ClientCreateDTO.model_validate(new_client_info, from_attributes=True)
    connect: ConnectSchema = await service.add_client(server_id, user, data)

    if connect:
        return {"status": "OK"}


@router.post("/{server_id}/client/update")
async def update_client_and_check(
        server_id: int,
        update_client_info: ClientUpdateRequest,
        user: UserSchema = Depends(get_current_active_user),
        service: PanelService = Depends(get_panel_service)
) -> dict[str, str]:

    data = ClientUpdateDTO.model_validate(update_client_info, from_attributes=True)
    connect = await service.update_client(server_id, user, data)

    if connect:
        return {"status": "OK"}


@router.post("/{server_id}/client/delete")
async def delete_client_and_check(
        server_id: int,
        delete_client_info: ClientDeleteRequest,
        user: UserSchema = Depends(get_current_active_user),
        panel_service: PanelService = Depends(get_panel_service),
        subscription_service: SubscriptionService = Depends(get_subscription_service)
) -> dict[str, str]:

    data = ClientDeleteDTO.model_validate(delete_client_info, from_attributes=True)
    await panel_service.delete_client(server_id, user, data)

    if subscription_service.delete_subscription(delete_client_info.sub_id):
        return {"status": "OK"}