from datetime import datetime

from pydantic import Field

from app.schema.base_schema import BaseSchema, ModelBaseInfo


class SubscriptionCreate(BaseSchema):
    email_name: str = Field(..., example="connect-example")
    url: str = Field(..., example="vless://16289ed8-3489-4f90...")
    user_id: int
    server_id: int
    end_date: datetime | None = None
    is_active: bool = True


class SubscriptionUpdate(BaseSchema):
    end_date: datetime | None = None
    is_active: bool | None = None


class SubscriptionSchema(BaseSchema):
    email_name: str
    url: str
    user_id: int
    server_id: int
    end_date: datetime | None = None
    is_active: bool


class SubscriptionModelSchema(ModelBaseInfo):
    email_name: str
    url: str
    user_id: int
    server_id: int
    end_date: datetime | None = None
    is_active: bool
