from sqlalchemy.orm import Mapped, mapped_column

from app.model.base_model import BaseModel
from app.schema.user_schema import User as UserSchema


class User(BaseModel):
    tg_id: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column()

    # def to_read_model(self) -> UserSchema:
    #     return UserSchema(
    #         id: int
    #         tg_id: int
    #         is_active: bool
    #         is_superuser: bool
    #         created_at: datetime
    #         updated_at: datetime
    #     )
