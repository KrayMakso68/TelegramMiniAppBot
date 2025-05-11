from datetime import datetime

from bot.schemas.base import BaseSchema, ModelBaseInfo
from bot.schemas.user import UserSchema


class SubscriptionUpdate(BaseSchema):
    end_date: datetime | None = None
    is_active: bool | None = None
    notified_3_days: bool = False
    notified_1_day: bool = False
    notified_expired: bool = False


class SubscriptionSchema(BaseSchema):
    id: int
    name: str
    email: str
    url: str
    user_id: int
    server_id: int
    end_date: datetime | None = None
    is_active: bool
    notified_3_days: bool
    notified_1_day: bool
    notified_expired: bool

    user_rel: UserSchema | None = None


class SubscriptionModelSchema(ModelBaseInfo):
    name: str
    email: str
    url: str
    user_id: int
    server_id: int
    end_date: datetime | None = None
    is_active: bool
    notified_3_days: bool
    notified_1_day: bool
    notified_expired: bool

    server_rel: UserSchema | None = None
