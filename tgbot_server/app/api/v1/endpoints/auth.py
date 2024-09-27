from fastapi import APIRouter, Depends
from app.schema.auth_schema import WebAppInitData, Token

router = APIRouter(
    prefix="/auth"
)


@router.post("/login")
def login(
        form_data: WebAppInitData = Depends()
) -> Token:
    pass
