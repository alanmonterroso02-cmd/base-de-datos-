import jwt
from datetime import datetime, timedelta, UTC

from config.config_app import config


def create_token(data: dict):
    payload = data.copy()

    payload["exp"] = datetime.now(UTC) + timedelta(minutes=25)
    payload["iat"] = datetime.now(UTC)

    return jwt.encode(
        payload,
        config.SECRET,
        algorithm="HS256"
    )


def validate_token(token: str):
    return jwt.decode(
        token,
        config.SECRET,
        algorithms=["HS256"]
    )