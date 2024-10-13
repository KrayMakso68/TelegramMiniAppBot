from init_data_py import InitData

from app.core.config import settings
from app.core.exceptions import WebAppValidationError
from app.schema.auth_schema import WebAppInitData, InitAuthData


def get_webapp_data(data: InitAuthData) -> WebAppInitData:
    bot_token: str = settings.BOT_TOKEN

    init_data = InitData.parse(data.query_string)

    if not init_data.validate(bot_token):
        raise WebAppValidationError("Invalid signature.")

    data_dict = init_data.to_dict()
    return WebAppInitData(**data_dict)




