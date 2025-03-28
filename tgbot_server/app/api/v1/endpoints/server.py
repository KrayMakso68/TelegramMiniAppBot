from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_active_user, get_server_service
from app.schema.server_schema import ServerInfo
from app.schema.user_schema import UserSchema
from app.services.server_service import ServerService

router = APIRouter(
    prefix="/server",
    tags=["server"]
)


@router.get("/all/available-info")
async def get_servers_short_info(
        user: UserSchema = Depends(get_current_active_user),
        service: ServerService = Depends(get_server_service)
) -> list[ServerInfo]:
    return await service.get_servers_short_info()
