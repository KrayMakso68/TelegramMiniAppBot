from enum import Enum

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
    operation_type: OperationType


class PaymentUpdate(BaseSchema):
    status: PaymentStatus


class PaymentSchema(ModelBaseInfo):
    user_id: int
    amount: float
    status: PaymentStatus
    operation_type: OperationType

