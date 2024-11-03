import uuid

from sqlalchemy import Integer, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.model.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    sub_uuid: Mapped[str] = mapped_column(String, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
