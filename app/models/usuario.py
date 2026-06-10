from enum import Enum
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class RolEnum(str, Enum):
    Admin = "Admin"
    Colaborador = "Colaborador"


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nombre_completo: str = Field(unique=True)
    correo: str = Field(unique=True)
    contrasena: str
    rol: RolEnum
    activo: bool = Field(default=True)
