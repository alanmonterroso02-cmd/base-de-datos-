from fastapi import APIRouter, Depends, Form, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.recicladores_repository import RecicladorRepository
from app.repositories.categorias_repository import CategoriaReciclajeRepository
from app.repositories.cupones_repository import CuponRepository
from app.repositories.usuarios_repository import UsuarioRepository
from app.services.recicladores_service import RecicladorService
from app.services.usuarios_service import UsuariosService
from app.schemas.usuario import UsuarioLogin

router = APIRouter(tags=["Autenticación"])


@router.post("/reciclador/login")
def login_reciclador(
    nit: int = Form(...),
    session: Session = Depends(get_session),
):
    reciclador_repo = RecicladorRepository(session)
    categoria_repo = CategoriaReciclajeRepository(session)
    cupon_repo = CuponRepository(session)
    service = RecicladorService(reciclador_repo, categoria_repo, cupon_repo)
    response = service.login(nit)
    if not response:
        raise HTTPException(status_code=404, detail="nit no encontrado")
    return response


@router.post("/usuarios/login")
def login_usuario(
    credenciales: UsuarioLogin,
    session: Session = Depends(get_session),
):
    repo = UsuarioRepository(session)
    service = UsuariosService(repo)
    return service.autenticar_usuario(credenciales.correo, credenciales.contrasena)
