import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Configs(BaseSettings):
    API: str = "/api"
    APP_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TelegramMiniAppBot"

    # database
    DATABASE_URI: str = "sqlite+aiosqlite:///sqlite.db"
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')

    # bot
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', "")

    # auth
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 60 minutes * 24 hours * 30 days = 30 days


configs = Configs()
