from pydantic import Field

from app.schema.base_schema import BaseSchema, ModelBaseInfo


# class ServerCreate(BaseSchema):
#     ...
#
#
# class ServerUpdate(BaseSchema):
#     ...


class ServerSchema(BaseSchema):
    id: int
    name: str = Field(..., example="Germany_kRayVPN_1")
    panel_url: str = Field(..., example="https://server_ip:panel_port/panel_path/")
    username: str
    password_enc: str
    subscription_url: str = Field(..., example="https://server_ip:sub_port/server_sub_path/")
    country_code: str = Field(..., example="RU, US, GB, etc.")
    is_active: bool


class ServerModelSchema(ModelBaseInfo):
    name: str
    panel_url: str
    username: str
    password_enc: str
    subscription_url: str
    country_code: str
    is_active: bool
