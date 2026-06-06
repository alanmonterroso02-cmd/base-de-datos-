from sqlmodel import create_engine
from config.config_app import config


DATABASE_URL = (
    f"mysql+pymysql://"
    f"{config.DB_USER}:"
    f"{config.DB_PASSWORD}@"
    f"{config.DB_HOST}:"
    f"{config.DB_PORT}/"
    f"{config.DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
