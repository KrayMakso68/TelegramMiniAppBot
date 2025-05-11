from decimal import Decimal

from pydantic import Field, ConfigDict

from bot.schemas.base import BaseSchema, ModelBaseInfo


class ServerSchema(BaseSchema):
    id: int
    name: str = Field(..., example="Germany_kRayVPN_1")
    panel_url: str = Field(..., example="https://server_ip:panel_port/panel_path/")
    username: str
    password_enc: str
    subscription_url: str = Field(..., example="https://server_ip:sub_port/server_sub_path/")
    month_price: Decimal = Field(..., gt=0, example="100.50")
    country_code: str = Field(..., example="ru, us, gb, etc.")
    is_active: bool


class ServerInfo(BaseSchema):
    id: int
    label: str = Field(..., alias="name", serialization_alias="label", example="Germany_kRayVPN_1")
    month_price: Decimal = Field(..., gt=0, example="100.50")
    country_code: str = Field(..., example="ru, us, gb, etc.")
    is_active: bool

    model_config = ConfigDict(
        json_encoders={
            Decimal: float
        }
    )


class ServerModelSchema(ModelBaseInfo):
    name: str
    panel_url: str
    username: str
    password_enc: str
    subscription_url: str
    country_code: str
    is_active: bool
