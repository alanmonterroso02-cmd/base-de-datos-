import secrets
from enum import Enum
from sqlmodel import SQLModel, Field


class RolEnum(Enum):
    Admin = "Admin"
    Usuario = "Usuario"


def generar_id() -> str:
    return str(secrets.randbelow(900_000_000_000) + 100_000_000_000)


class UsuariosModel(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: str = Field(default_factory=generar_id, primary_key=True)

    nombre_completo: str = Field(unique=True)
    correo: str = Field(unique=True)
    pin: str
    rol: RolEnum
