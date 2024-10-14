from app.schema.base_schema import BaseSchema


class InitAuthData(BaseSchema):
    query_string: str


class WebAppUser(BaseSchema):
    id: int
    is_bot: bool | None = None
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None


class WebAppChat(BaseSchema):
    id: int
    type: str
    title: str
    username: str | None = None
    photo_url: str | None = None


class WebAppInitData(BaseSchema):
    query_id: str | None = None
    user: WebAppUser | None = None
    receiver: WebAppUser | None = None
    chat: WebAppChat | None = None
    chat_type: str | None = None
    chat_instance: str | None = None
    start_param: str | None = None
    can_send_after: int | None = None
    auth_date: int
    hash: str


class TokenInfo(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    tg_id: int
