from pydantic import BaseModel, EmailStr
from app.models.usuario_model import RolEnum

class UsuarioCreate(BaseModel):
    nombre_completo: str
    correo: EmailStr
    contrasena: str
    rol: RolEnum
