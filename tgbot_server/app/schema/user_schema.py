from app.schema.base_schema import ModelBaseInfo, BaseSchema


class UserCreate(BaseSchema):
    tg_id: int


class UserSchema(ModelBaseInfo, UserCreate):
    sub_uuid: str
    is_active: bool
    is_superuser: bool
