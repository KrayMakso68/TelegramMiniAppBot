import enum

from sqlalchemy import Integer, Float, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base_model import BaseModel


class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OperationType(enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class Payment(BaseModel):
    __tablename__ = 'payments'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.PENDING
    )
    operation_type: Mapped[OperationType] = mapped_column(
        Enum(OperationType, name="operation_type_enum"),
        nullable=False
    )

    user_rel = relationship("User", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, status={self.status}, created_at={self.created_at})>"


class PaymentOptions(BaseModel):
    __tablename__ = 'payment_options'

    label: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
