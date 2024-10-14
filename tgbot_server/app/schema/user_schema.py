from app.schema.base_schema import ModelBaseInfo, BaseSchema


class UserCreate(BaseSchema):
    tg_id: int
    is_active: bool = True
    is_superuser: bool = False


class UserSchema(ModelBaseInfo, UserCreate):
    ...
