import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

DB_HOST: str = os.getenv('DB_HOST')
DB_PORT: str = os.getenv('DB_PORT')
DB_NAME: str = os.getenv('DB_NAME')
DB_USER: str = os.getenv('DB_USER')
DB_PASSWORD: str = os.getenv('DB_PASSWORD')


@dataclass
class Config:
    TOKEN: str = os.getenv("TOKEN")
    WEBAPP_URL: str = os.getenv("WEBAPP_URL")
    DB_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


config = Config()
