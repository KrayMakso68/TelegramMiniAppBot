from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.core.dependencies import get_current_active_user, get_payment_service
from app.schema.payment_schema import PaymentRequest
from app.schema.user_schema import UserSchema
from app.services.payment_service import PaymentService
from app.utils import validate_yoomoney

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
async def check_yoomoney_payment(
        request: Request,
        service: PaymentService = Depends(get_payment_service)
):
    form_data = await request.form()
    if validate_yoomoney.verify_hash(form_data):
        payment_id = int(form_data.get("label"))
        amount = float(form_data.get("withdraw_amount"))
        await service.processing_payment(payment_id, amount)
        return {"status": "OK"}
    else:
        return {"status": "Error"}
