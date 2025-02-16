import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    API: str = "/api"
    APP_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TelegramMiniAppBot"

    # database
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # bot
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')

    # auth
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)

    # payment
    YOOMONEY_WALLET: int = os.getenv('YOOMONEY_WALLET')
    YOOMONEY_SECRET: str = os.getenv('YOOMONEY_SECRET')
    PAY_SUCCESS_URL: str = os.getenv('PAY_SUCCESS_URL')

    # # CORS
    # ALLOWED_ORIGINS: list[str] = [url for url in os.getenv('ALLOWED_ORIGINS', "*").split(',')]

    # 3x-ui
    TLS_VERIFY: bool = False
    PANEL_HOST: str = os.getenv("PANEL_HOST")
    PANEL_USERNAME: str = os.getenv("PANEL_USERNAME")
    PANEL_PASSWORD: str = os.getenv("PANEL_PASSWORD")
    SUBSCRIPTION_API_PORT: str = os.getenv("SUBSCRIPTION_API_PORT")
    SUBSCRIPTION_API_PATH: str = os.getenv("SUBSCRIPTION_API_PATH")


settings = Settings()
