from typing import Optional
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

load_dotenv("./system_configs/.env")


class Settings(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    APP_TITLE: str = "TODO API"
    # DATABASE
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_URL: Optional[str]
    # JWT
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 31  # 31 days

    @validator("DB_URL", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: dict[str, str]
    ) -> str:
        if isinstance(v, str):
            return v
        return (
            f"{values['DB_HOST']}{values['DB_USER']}:{values['DB_PASSWORD']}"
            f"@{values['DB_NAME']}:{values['DB_PORT']}"
        )


settings = Settings()
