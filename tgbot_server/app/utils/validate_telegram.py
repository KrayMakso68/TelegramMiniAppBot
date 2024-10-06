import hashlib
import hmac
from operator import itemgetter
import time

from app.core.exceptions import WebAppValidationError
from app.schema.auth_schema import WebAppInitData


def check_webapp_signature(token: str, init_data: WebAppInitData) -> bool:
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    :param token: str
    :param init_data: WebAppInitData
    :return:
    """
    parsed_data = init_data.model_dump()

    if "hash" not in parsed_data:
        raise WebAppValidationError("Hash is not present in init data.")
    auth_date = parsed_data.get('auth_date')
    if _verify_telegram_session_outdate(auth_date):
        raise WebAppValidationError("Telegram authentication session is expired.")

    hash_ = parsed_data.pop('hash')
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    if calculated_hash != hash_:
        raise WebAppValidationError("Invalid signature.")

    return True


def _verify_telegram_session_outdate(auth_date: str) -> bool:
    one_day_in_second = 86400
    unix_time_now = int(time.time())
    unix_time_auth_date = int(auth_date)
    timedelta = unix_time_now - unix_time_auth_date

    if timedelta > one_day_in_second:
        return True
    return False
