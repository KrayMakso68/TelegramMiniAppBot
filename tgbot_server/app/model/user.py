from sqlalchemy.orm import Mapped, mapped_column

from app.model.base_model import BaseModel
from app.schema.user_schema import User as UserSchema


class User(BaseModel):
    __tablename__ = 'user'

    tg_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column()

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            tg_id=self.tg_id,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
