import urllib.parse

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from app.core.dependencies import get_subscription_service_for_user
from app.schema.connect_schema import ConnectSchema
from app.services.subscription_service import SubscriptionService

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"]
)


@router.get("/subscriptions")
async def get_user_subscriptions(service: SubscriptionService = Depends(get_subscription_service_for_user)) -> list[ConnectSchema]:
    return await service.get_user_connects()


@router.get("/import-config")
async def import_config(config: str):
    encoded_config = urllib.parse.quote(config)
    config_url = f"hiddify://install-config?url={encoded_config}"
    return RedirectResponse(url=config_url)
