from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.usuarios_repository import UsuarioRepository
from app.services.usuarios_service import UsuariosService
from app.schemas.usuario import UsuarioCreate
from app.utils.auth import get_current_usuario, require_admin

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


@router.get("/perfil")
def perfil_usuario(
    usuario: dict = Depends(get_current_usuario),
    service: UsuariosService = Depends(get_usuarios_service),
):
    user = service.obtener_usuario_por_id(usuario["id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return {
        "nombre_completo": user.nombre_completo,
        "correo": user.correo,
        "rol": user.rol.value,
    }


@router.get("/list")
def listar_usuarios(
    _: dict = Depends(require_admin),
    service: UsuariosService = Depends(get_usuarios_service),
):
    return service.listar_usuarios()


@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: UUID,
    _: dict = Depends(require_admin),
    service: UsuariosService = Depends(get_usuarios_service),
):
    return service.eliminar_usuario(str(usuario_id))


@router.patch("/{usuario_id}/reactivar")
def reactivar_usuario(
    usuario_id: UUID,
    _: dict = Depends(require_admin),
    service: UsuariosService = Depends(get_usuarios_service),
):
    return service.reactivar_usuario(str(usuario_id))
