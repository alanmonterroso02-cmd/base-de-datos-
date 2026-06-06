import bcrypt


class PasswordService:
    @classmethod
    def hash(cls, value: str):
        return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode(
            "utf-8"
        )

    @classmethod
    def verify(cls, plain_value: str, hashed_value: str):
        return bcrypt.checkpw(plain_value.encode("utf-8"), hashed_value.encode("utf-8"))
