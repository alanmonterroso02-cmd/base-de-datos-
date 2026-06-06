from typing import Literal
from pydantic import BaseModel, Field


class LoginRequestSchema(BaseModel):
    token: str = Field(
        min_length=1,
        max_length=255,
        description="Identificador del usuario (ID o token de acceso).",
        example="25559584554",
    )

    pin: str = Field(
        min_length=1,
        max_length=255,
        description="PIN numérico del usuario para autenticación.",
        example="1236952",
    )


    mode: Literal["web", "esp32"] = Field(
        default="web",
        description="Tipo de autenticación: web o esp32",
    )
