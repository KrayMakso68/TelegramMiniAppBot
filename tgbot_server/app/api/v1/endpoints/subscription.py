from fastapi import APIRouter, Depends

from app.api.dependencies import get_subscription_service, get_current_active_user
from app.schema.subscription_schema import SubscriptionSchema
from app.schema.user_schema import UserSchema
from app.services.subscription_service import SubscriptionService

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"]
)


@router.get("/servers")
async def get_user_subscriptions_by_server(
        user: UserSchema = Depends(get_current_active_user),
        service: SubscriptionService = Depends(get_subscription_service)
) -> dict[str, list[SubscriptionSchema]]:
    return await service.user_subscriptions_filtered_by_server(user.id)


# @router.get("/import-config")
# async def import_config(config: str):
#     encoded_config = urllib.parse.quote(config)
#     config_url = f"hiddify://install-config?url={encoded_config}"
#     return RedirectResponse(url=config_url)
