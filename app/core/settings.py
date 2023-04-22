from typing import Optional, Any

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv("./system_configs/.env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int


settings = Settings()
