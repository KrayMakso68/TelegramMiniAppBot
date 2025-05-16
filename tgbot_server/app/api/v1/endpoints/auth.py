from fastapi import APIRouter, Depends

from app.schema.auth_schema import TokenInfo, InitAuthData
from app.api.dependencies import get_auth_service
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
async def login_for_access_token(
        init_data: InitAuthData,
        service: AuthService = Depends(get_auth_service)
) -> TokenInfo:
    return await service.login(init_data)
