import enum

from sqlalchemy import Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base_model import BaseModel


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Payment(BaseModel):
    __tablename__ = 'payments'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    user = relationship("User", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, status={self.status}, created_at={self.created_at})>"
