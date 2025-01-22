from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

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
) -> JSONResponse:
    user_avatar_base64 = await service.get_user_avatar(current_user.tg_id)
    return JSONResponse(content=f"data:image/jpeg;base64,{user_avatar_base64}")


@router.get("/balance")
async def get_user_balance(
        current_user: UserSchema = Depends(get_current_active_user),
) -> float:
    return current_user.balance
