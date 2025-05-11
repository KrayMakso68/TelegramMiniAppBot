from bot.schemas.base import ModelBaseInfo


class UserSchema(ModelBaseInfo):
    tg_id: int
    sub_uuid: str
    balance: float
    is_active: bool
    is_superuser: bool
