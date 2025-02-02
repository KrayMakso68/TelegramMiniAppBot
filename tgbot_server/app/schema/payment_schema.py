from enum import Enum
from datetime import datetime

from app.schema.base_schema import BaseSchema, ModelBaseInfo


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class PaymentRequest(BaseSchema):
    amount: float


class PaymentCreate(BaseSchema):
    user_id: int
    amount: float
    title: str | None = None
    operation_type: OperationType


class PaymentUpdate(BaseSchema):
    status: PaymentStatus


class PaymentSchema(ModelBaseInfo):
    user_id: int
    amount: float
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
