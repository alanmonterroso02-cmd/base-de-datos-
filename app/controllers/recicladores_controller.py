from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlmodel import Session

from app.core.database import get_session
from app.utils.auth import get_current_reciclador, require_colaborador
from app.repositories.recicladores_repository import RecicladorRepository
from app.repositories.categorias_repository import CategoriaReciclajeRepository
from app.repositories.cupones_repository import CuponRepository
from app.services.recicladores_service import RecicladorService
from app.schemas.material_reciclado import MaterialRecicladoSchema
from app.schemas.reciclador import RecicladorCreate

reciclador_router = APIRouter(prefix="/reciclador", tags=["Reciclador"])


def get_reciclador_service(session: Session = Depends(get_session)):
    reciclador_repo = RecicladorRepository(session)
    categoria_repo = CategoriaReciclajeRepository(session)
    cupon_repo = CuponRepository(session)
    return RecicladorService(reciclador_repo, categoria_repo, cupon_repo)


@reciclador_router.post("/login")
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


@reciclador_router.post("/puntos/agregar")
def agregar_puntos(
    data: MaterialRecicladoSchema,
    reciclador=Depends(get_current_reciclador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.agregar_puntos(reciclador["nit"], data)


@reciclador_router.get("/perfil")
def ver_perfil(
    reciclador=Depends(get_current_reciclador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.ver_perfil(reciclador["nit"])


@reciclador_router.get("/puntos/historial")
def ver_historial_puntos(
    reciclador=Depends(get_current_reciclador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.ver_historial_puntos(reciclador["nit"])


@reciclador_router.get("/cupones")
def ver_cupones(
    reciclador=Depends(get_current_reciclador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.listar_cupones(reciclador["nit"])


@reciclador_router.get("/admin/list")
def listar_recicladores_admin(
    _: dict = Depends(require_colaborador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.listar_todos()


@reciclador_router.post("/admin/create")
def crear_reciclador_admin(
    data: RecicladorCreate,
    _: dict = Depends(require_colaborador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.crear_reciclador(data)


@reciclador_router.post("/admin/create-batch")
def crear_recicladores_masivo_admin(
    data: list[RecicladorCreate],
    _: dict = Depends(require_colaborador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.crear_recicladores_masivo(data)


@reciclador_router.get("/admin/{nit}")
def detalle_reciclador_admin(
    nit: int,
    _: dict = Depends(require_colaborador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.obtener_detalle_admin(nit)
