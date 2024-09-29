from fastapi import APIRouter, Depends

from app.schema.auth_schema import WebAppInitData, Token
from app.core.dependencies import auth_service
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(
        auth_data: WebAppInitData,
        service: AuthService = Depends(auth_service)
) -> Token:
    return service.login(auth_data)

# Token(access_token=access_token, token_type="bearer")