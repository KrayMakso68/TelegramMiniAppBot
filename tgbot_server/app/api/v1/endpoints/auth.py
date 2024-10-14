from fastapi import APIRouter, Depends

from app.schema.auth_schema import TokenInfo, InitAuthData
from app.schema.user_schema import UserSchema
from app.core.dependencies import get_auth_service, get_current_active_user
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
async def login_for_access_token(
        init_data: InitAuthData = Depends(),
        service: AuthService = Depends(get_auth_service)
) -> TokenInfo:
    return await service.login(init_data)


@router.get("/user")
async def user(
        current_user: UserSchema = Depends(get_current_active_user)
) -> UserSchema:
    return current_user
