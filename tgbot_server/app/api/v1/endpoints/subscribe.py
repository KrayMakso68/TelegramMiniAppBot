from fastapi import APIRouter, Depends

from app.core.dependencies import get_subscribe_service_for_user
from app.schema.subscribe_schema import ConnectSchema
from app.services.subscribe_service import SubscribeService

router = APIRouter(
    prefix="/subscribe",
    tags=["subscribe"]
)


@router.get("/connects")
async def get_user_subscribes(service: SubscribeService = Depends(get_subscribe_service_for_user)) -> list[ConnectSchema]:
    return await service.get_user_connects()
