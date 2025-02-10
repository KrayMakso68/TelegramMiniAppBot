from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model import BaseModel


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    email_name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    server_id: Mapped[int] = mapped_column(Integer, ForeignKey("servers.id"), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    server_rel = relationship("Server", back_populates="subscriptions")
    user_rel = relationship("User", back_populates="subscriptions")

