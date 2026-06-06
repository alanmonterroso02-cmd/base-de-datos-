from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigApp(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    # DB
    DB_NAME: str = "app_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "app_user"
    DB_PASSWORD: str = "app123"
    # Email
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 465
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    # jwt
    SECRET: str


templates = Jinja2Templates(directory="templates")
config = ConfigApp()
