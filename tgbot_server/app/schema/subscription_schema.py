from datetime import datetime

from pydantic import Field

from app.schema.base_schema import BaseSchema, ModelBaseInfo


class SubscriptionCreate(BaseSchema):
    name: str = Field(..., example="connect-example")
    email: str = Field(..., example="connect-name@connect-uuid (uuid with '_')")
    url: str = Field(..., example="vless://16289ed8-3489-4f90...")
    user_id: int
    server_id: int
    end_date: datetime | None = None
    is_active: bool = True


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


class SubscriptionModelSchema(ModelBaseInfo):
    name: str
    email: str
    url: str
    user_id: int
    server_id: int
    end_date: datetime | None = None
    is_active: bool
    notified_3_days: bool = False
    notified_1_day: bool = False
    notified_expired: bool = False
