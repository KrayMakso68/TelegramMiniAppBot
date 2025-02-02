from datetime import datetime

from fastapi import APIRouter, Depends, Form

from app.core.dependencies import get_current_active_user, get_payment_service
from app.schema.payment_schema import PaymentRequest, PaymentSchema, YooMoneyData, PaymentOptionSchema
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
        notification_type: str = Form(...),
        operation_id: str = Form(...),
        amount: float = Form(...),
        withdraw_amount: float = Form(...),
        currency: str = Form(...),
        datetime: datetime = Form(...),
        sender: str = Form(''),
        codepro: bool = Form(...),
        label: str = Form(''),
        sha1_hash: str = Form(...),
        unaccepted: bool = Form(False),
        service: PaymentService = Depends(get_payment_service)
):
    data = YooMoneyData(
        notification_type=notification_type,
        operation_id=operation_id,
        amount=amount,
        withdraw_amount=withdraw_amount,
        currency=currency,
        datetime=datetime,
        sender=sender,
        codepro=codepro,
        label=label,
        sha1_hash=sha1_hash,
        unaccepted=unaccepted
    )
    return await service.processing_yoomoney_payment(data)


@router.get("/history")
async def get_user_payments_history_by_day(
        user: UserSchema = Depends(get_current_active_user),
        service: PaymentService = Depends(get_payment_service)
) -> dict[str, list[PaymentSchema]]:
    return await service.get_group_payments_by_day(user.id)


@router.get("/options")
async def get_payment_options(
        user: UserSchema = Depends(get_current_active_user),
        service: PaymentService = Depends(get_payment_service)
) -> list[PaymentOptionSchema]:
    return await service.get_payment_options()
