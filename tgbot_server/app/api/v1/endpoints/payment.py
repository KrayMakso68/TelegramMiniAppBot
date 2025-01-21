from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.core.dependencies import get_current_active_user
from app.schema.payment_schema import PaymentRequest
from app.schema.user_schema import UserSchema

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)


@router.post("/new/yoomoney")
async def new_yoomoney_payment(
        request: PaymentRequest,
        user: UserSchema = Depends(get_current_active_user),
        service: PaymentService = Depends(get_payment_service)
) -> RedirectResponse:

    payment_url = await service.new_yoomoney_payment(user.id, request.amount)

    return RedirectResponse(url=payment_url)


@router.post("/check/yoomoney")
async def check_yoomoney_payment():
    return await None