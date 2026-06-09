from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from app.service.usuarios_service import UsuariosService
from app.schema.usuario import UsuarioCreate, UsuarioLogin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_usuarios_service(session: Session = Depends(get_session)):
    return UsuariosService(session)

@router.post("/registro", status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    usuario: UsuarioCreate,
    service: UsuariosService = Depends(get_usuarios_service)
):
    """Registra un nuevo usuario en el sistema."""
    return service.registrar_usuario(usuario)

@router.post("/login")
async def login_usuario(
    credenciales: UsuarioLogin,
    service: UsuariosService = Depends(get_usuarios_service)
):
    """Autentica a un usuario y devuelve un token JWT."""
    return service.autenticar_usuario(credenciales.correo, credenciales.contrasena)
