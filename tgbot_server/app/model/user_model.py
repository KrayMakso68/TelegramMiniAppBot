from sqlalchemy.orm import Mapped, mapped_column

from app.model.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    tg_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column()

    class Config:
        orm_mode = True
