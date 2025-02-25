from fastapi import APIRouter, Depends

from app.core.dependencies import get_panel_service, get_current_active_user
from app.schema.panel_schema import ClientSchema
from app.schema.user_schema import UserSchema
from app.services.panel_service import PanelService

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
):
    await service.update_user_subscriptions(user)
    return {"message": "Subscriptions updated successfully"}
