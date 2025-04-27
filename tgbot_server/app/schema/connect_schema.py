from datetime import timedelta
import re

from pydantic import model_validator
from urllib.parse import urlparse, unquote

from app.schema.base_schema import BaseSchema


class ConnectSchema(BaseSchema):
    connect_url: str
    uuid: str
    name: str
    email: str
    inbound_name: str
    remaining_seconds: int | None
    active: bool

    @model_validator(mode="before")
    @classmethod
    def check_fields_not_empty(cls, values):
        required_fields = ['connect_url', 'uuid', 'name', 'email', 'inbound_name', 'active']
        for field in required_fields:
            if values.get(field) is None:
                raise ValueError(f"Field {field} cannot be empty!")
        return values

    @classmethod
    def from_url(cls, url: str):
        parsed_url = urlparse(url)
        fragment = unquote(parsed_url.fragment).split("-")

        if not fragment or len(fragment) == 0:
            raise ValueError("Invalid fragment in URL.")

        if "N/A" in fragment[0] or "⛔" in fragment[0]:
            active = False
            remaining_seconds = 0
        elif len(fragment) > 2:
            time_string = fragment[2]
            remaining_seconds = cls._extract_remaining_seconds(time_string)
            active = True
        else:
            remaining_seconds = None
            active = True

        cleaned_fragment = cls._clean_fragment(fragment)
        cleaned_url = url.replace(f"#{parsed_url.fragment}", f"#{cleaned_fragment}")

        inbound_name, email, name = cls._extract_name_email(cleaned_fragment)

        return cls(
            connect_url=cleaned_url,
            uuid=parsed_url.username,
            inbound_name=inbound_name,
            email=email,
            name=name,
            remaining_seconds=remaining_seconds,
            active=active
        )

    @staticmethod
    def _extract_remaining_seconds(time_string: str) -> int:
        """Извлекает оставшееся время в секундах из строки времени."""
        try:
            days_match = re.search(r'(\d+)D', time_string)
            hours_match = re.search(r'(\d+)H', time_string)
            days = int(days_match.group(1)) if days_match else 0
            hours = int(hours_match.group(1)) if hours_match else 0
            return int(timedelta(days=days, hours=hours).total_seconds())
        except Exception as e:
            raise ValueError(f"Invalid time format: {time_string}") from e

    @staticmethod
    def _clean_fragment(fragment: list) -> str:
        """Очищает фрагмент, убирая лишние символы."""
        if len(fragment) == 0:
            return "unknown"
        if fragment[0].startswith("⛔") or fragment[0].startswith('%'):
            return '-'.join(fragment[1:3])
        return '-'.join(fragment[:2]) if len(fragment) > 1 else fragment[0]

    @staticmethod
    def _extract_name_email(cleaned_fragment: str) -> tuple:
        """Извлекает имя и email из очищенного фрагмента."""
        parts = cleaned_fragment.split("-")
        inbound_name = parts[0] if len(parts) > 0 else 'unknown'
        email = parts[1] if len(parts) > 1 else 'unknown'
        name = ''

        if '@' in email:
            name = parts[1].split('@')[0]
        else:
            name = email

        return inbound_name, email, name
