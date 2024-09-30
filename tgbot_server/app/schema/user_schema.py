from pydantic import BaseModel

from app.schema.base_schema import ModelBaseInfo


class UserSchema(BaseModel):
    tg_id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class User(ModelBaseInfo, UserSchema):
    ...
