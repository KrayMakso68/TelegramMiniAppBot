import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Configs(BaseSettings):
    API: str = "/api"
    APP_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TelegramMiniAppBot"
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')


configs = Configs()
