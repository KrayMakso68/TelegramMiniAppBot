import hashlib

from app.core.config import settings
from app.schema.payment_schema import YooMoneyData


def verify_hash(data: YooMoneyData) -> bool:
    hash_string = "&".join([
        data.notification_type,
        data.operation_id,
        f"{data.amount:.2f}",
        str(data.currency),
        data.datetime.isoformat(),
        data.sender or "",
        "true" if data.codepro else "false",
        settings.YOOMONEY_SECRET,
        data.label or ""
    ])

    calculated_hash = hashlib.sha1(hash_string.encode("utf-8")).hexdigest()

    return calculated_hash.lower() == data.sha1_hash.lower()

