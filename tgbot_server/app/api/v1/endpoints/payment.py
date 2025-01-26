from datetime import datetime

from fastapi import APIRouter, Depends, Request

from app.core.dependencies import get_current_active_user, get_payment_service
from app.schema.payment_schema import PaymentRequest, PaymentSchema
from app.schema.user_schema import UserSchema
from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)


@router.post("/new/yoomoney")
async def new_yoomoney_payment(
        request: PaymentRequest,
        user: UserSchema = Depends(get_current_active_user),
        service: PaymentService = Depends(get_payment_service)
) -> str:
    return await service.new_yoomoney_payment(user.id, request.amount)


@router.post("/check/yoomoney")
async def check_yoomoney_payment(
        request: Request,
        service: PaymentService = Depends(get_payment_service)
):
    form_data = await request.form()
    return await service.processing_yoomoney_payment(form_data)


@router.get("/history")
async def get_user_payments_history_by_day(
        user: UserSchema = Depends(get_current_active_user),
        service: PaymentService = Depends(get_payment_service)
) -> dict[str, list[PaymentSchema]]:
    return await service.get_group_payments_by_day(user.id)
