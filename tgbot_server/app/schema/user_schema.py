from pydantic import BaseModel

from app.schema.base_schema import ModelBaseInfo


class UserCreate(BaseModel):
    tg_id: int
    is_active: bool = True
    is_superuser: bool = False


class UserSchema(ModelBaseInfo, UserCreate):
    ...
