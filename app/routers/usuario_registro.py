from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.usuarios_repository import UsuarioRepository
from app.services.usuarios_service import UsuariosService
from app.schemas.usuario import UsuarioCreate
from app.utils.auth import require_admin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_usuarios_service(session: Session = Depends(get_session)):
    repo = UsuarioRepository(session)
    return UsuariosService(repo)


@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: UsuarioCreate,
    _: dict = Depends(require_admin),
    service: UsuariosService = Depends(get_usuarios_service),
):
    return service.registrar_usuario(usuario)
