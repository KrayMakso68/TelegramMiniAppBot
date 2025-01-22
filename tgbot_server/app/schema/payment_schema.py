from enum import Enum

from app.schema.base_schema import BaseSchema, ModelBaseInfo


class PaymentRequest(BaseSchema):
    amount: float


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class OperationType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class PaymentSchema(BaseSchema, ModelBaseInfo):
    user_id: int
    amount: float
    status: PaymentStatus
    operation_type: OperationType
