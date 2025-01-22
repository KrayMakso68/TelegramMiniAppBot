import hashlib

from starlette.datastructures import FormData
from app.core.config import settings


def verify_hash(data: FormData) -> bool:
    received_hash = data.get("sha1_hash")
    if not received_hash:
        return False

    hash_string = "&".join([
        data.get("notification_type", ""),
        data.get("operation_id", ""),
        data.get("amount", ""),
        data.get("currency", ""),
        data.get("datetime", ""),
        data.get("sender", ""),
        data.get("codepro", ""),
        settings.YOOMONEY_SECRET,
        data.get("label", ""),
    ])

    calculated_hash = hashlib.sha1(hash_string.encode("utf-8")).hexdigest()

    return calculated_hash == received_hash
