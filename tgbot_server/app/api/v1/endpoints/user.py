from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.core.dependencies import get_current_active_user
from app.core.dependencies import get_user_service
from app.schema.user_schema import UserSchema
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("")
async def get_current_user(
        user: UserSchema = Depends(get_current_active_user)
) -> UserSchema:
    return user


@router.get("/avatar")
async def user_avatar(
        current_user: UserSchema = Depends(get_current_active_user),
        service: UserService = Depends(get_user_service)
) -> StreamingResponse:
    return await service.get_user_avatar(current_user.tg_id)
