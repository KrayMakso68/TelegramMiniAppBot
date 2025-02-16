from fastapi import APIRouter, Depends

from app.core.dependencies import get_panel_service
from app.schema.panel_schema import ClientSchema
from app.services.panel_service import PanelService

router = APIRouter(
    prefix="/panel",
    tags=["panel"]
)


@router.get("/client/info_by_uuid/{client_uuid}")
async def get_clients_by_uuid(
        client_uuid: str,
        service: PanelService = Depends(get_panel_service)
) -> list[ClientSchema]:
    return await service.get_client_info_by_id(client_uuid)


@router.get("/client/info_by_email/{client_email}")
async def get_client_by_email(
        client_email: str,
        service: PanelService = Depends(get_panel_service)
) -> ClientSchema:
    return await service.get_client_info_by_email(client_email)


@router.put("/subscription/{sub_uuid}")
async def update_clients():
    ...
