from fastapi import APIRouter, Depends

from app.core.dependencies import get_subscribe_service_for_user
from app.services.subscribe_service import SubscribeService

router = APIRouter(
    prefix="/subscribes",
    tags=["subscribes"]
)


@router.get("")
async def get_user_subscribes(service: SubscribeService = Depends(get_subscribe_service_for_user)) -> list:
    return await service.get_user_subscribes()
