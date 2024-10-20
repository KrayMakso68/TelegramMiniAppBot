import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

TOKEN: str = os.getenv('TOKEN')
WEBAPP_URL: str = os.getenv('WEBAPP_URL')