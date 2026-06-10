from pydantic import BaseModel, EmailStr
from app.models.usuario import RolEnum


class UsuarioCreate(BaseModel):
    nombre_completo: str
    correo: EmailStr
    contrasena: str
    rol: RolEnum


class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str
