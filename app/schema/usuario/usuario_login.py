from pydantic import BaseModel, EmailStr

class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str
