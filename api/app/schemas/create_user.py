from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateUserRequestSchema(BaseModel):
    nombre_completo: str = Field(
        min_length=2,
        max_length=255,
        description="Nombre completo del usuario (no puede estar vacío).",
        example="Juan Pérez",
    )

    correo: EmailStr = Field(
        description="Correo electrónico válido del usuario.", example="juan@example.com"
    )
