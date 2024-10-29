from py3xui import AsyncApi
from app.core.config import settings


class XUIService:
    def __init__(self):
        self.api = AsyncApi(settings.XUI_HOST, settings.XUI_USERNAME, settings.XUI_PASSWORD)
