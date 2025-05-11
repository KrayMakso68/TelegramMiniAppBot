import uuid

from sqlalchemy import Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    sub_uuid: Mapped[str] = mapped_column(String, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    balance: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), default=0.00)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    subscriptions = relationship("Subscription", back_populates="user_rel")
