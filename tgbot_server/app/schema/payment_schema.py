from decimal import Decimal
from enum import Enum
from datetime import datetime

from pydantic import Field

from app.schema.base_schema import BaseSchema, ModelBaseInfo


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class PaymentRequest(BaseSchema):
    amount: Decimal = Field(..., gt=0, example="100.50")


class PaymentCreate(BaseSchema):
    user_id: int
    amount: Decimal = Field(..., gt=0, example="100.50")
    status: PaymentStatus = Field(PaymentStatus.PENDING, example="PENDING, COMPLETED, FAILED")
    title: str | None = Field(None, example="Оплата подписки")
    operation_type: OperationType


class PaymentUpdate(BaseSchema):
    status: PaymentStatus


class PaymentSchema(ModelBaseInfo):
    user_id: int
    amount: Decimal
    status: PaymentStatus
    title: str | None = None
    operation_type: OperationType


class YooMoneyData(BaseSchema):
    notification_type: str
    operation_id: str
    amount: float
    withdraw_amount: float
    currency: str
    datetime: datetime
    sender: str = ''
    codepro: bool
    label: str = ''
    sha1_hash: str
    unaccepted: bool = False


class PaymentOptionSchema(BaseSchema):
    label: str
    path: str
    

class PaymentOptionBase(ModelBaseInfo):
    label: str
    path: str
