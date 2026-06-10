import jwt
from datetime import datetime, timedelta, UTC

from app.core.settings import settings


def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(UTC) + timedelta(minutes=25)
    payload["iat"] = datetime.now(UTC)
    return jwt.encode(payload, settings.SECRET, algorithm="HS256")


def validate_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET, algorithms=["HS256"])
