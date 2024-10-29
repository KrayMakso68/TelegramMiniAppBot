import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent

DB_PATH = BASE_DIR / "sqlite.db"


class Settings(BaseSettings):
    API: str = "/api"
    APP_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TelegramMiniAppBot"

    # database
    DATABASE_URL: str = f"sqlite+aiosqlite:///{DB_PATH}"
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')

    # bot
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')

    # auth
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)

    # # CORS
    # ALLOWED_ORIGINS: list[str] = [url for url in os.getenv('ALLOWED_ORIGINS', "*").split(',')]

    # 3x-ui
    XUI_HOST: str = os.getenv("XUI_HOST")
    XUI_USERNAME: str = os.getenv("XUI_USERNAME")
    XUI_PASSWORD: str = os.getenv("XUI_PASSWORD")


settings = Settings()
