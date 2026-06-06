import jwt
from datetime import datetime, timedelta, timezone

# config
from config.config_app import config


class JWTService:
    @classmethod
    def create_token(cls, user_id: str, role: str, mode: str) -> str:
        expire_minutes = 10 if mode == "esp32" else 12 * 60

        payload = {
            "sub": user_id,
            "role": role,
            "type": mode,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=expire_minutes),
        }

        return jwt.encode(payload, config.SECRET, algorithm="HS256")
