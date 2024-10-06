from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.model.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
