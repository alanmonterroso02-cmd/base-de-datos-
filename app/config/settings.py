from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )

    DB_NAME: str = "app_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3307
    DB_USER: str = "app_user"
    DB_PASSWORD: str = "app123"
    SECRET: str = "dev-secret-change-in-production"


settings = Settings()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
