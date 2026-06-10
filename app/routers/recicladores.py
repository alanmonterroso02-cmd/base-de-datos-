from fastapi import APIRouter, Depends, Form, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.utils.auth import get_current_reciclador, require_colaborador
from app.repositories.recicladores_repository import RecicladorRepository
from app.repositories.categorias_repository import CategoriaReciclajeRepository
from app.repositories.cupones_repository import CuponRepository
from app.services.recicladores_service import RecicladorService
from app.schemas.material_reciclado import MaterialRecicladoSchema
from app.schemas.reciclador import RecicladorCreate

router = APIRouter(prefix="/reciclador", tags=["Reciclador"])


def get_reciclador_service(session: Session = Depends(get_session)):
    reciclador_repo = RecicladorRepository(session)
    categoria_repo = CategoriaReciclajeRepository(session)
    cupon_repo = CuponRepository(session)
    return RecicladorService(reciclador_repo, categoria_repo, cupon_repo)


@router.post("/puntos/agregar")
def agregar_puntos(
    data: MaterialRecicladoSchema,
    reciclador=Depends(get_current_reciclador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.agregar_puntos(reciclador["nit"], data)


@router.get("/perfil")
def ver_perfil(
    reciclador=Depends(get_current_reciclador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.ver_perfil(reciclador["nit"])


@router.get("/puntos/historial")
def ver_historial_puntos(
    reciclador=Depends(get_current_reciclador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.ver_historial_puntos(reciclador["nit"])


@router.get("/cupones")
def ver_cupones(
    reciclador=Depends(get_current_reciclador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.listar_cupones(reciclador["nit"])


@router.get("/admin/list")
def listar_recicladores_admin(
    _: dict = Depends(require_colaborador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.listar_todos()


@router.post("/admin/create")
def crear_reciclador_admin(
    data: RecicladorCreate,
    _: dict = Depends(require_colaborador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.crear_reciclador(data)


@router.post("/admin/create-batch")
def crear_recicladores_masivo_admin(
    data: list[RecicladorCreate],
    _: dict = Depends(require_colaborador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.crear_recicladores_masivo(data)


@router.get("/admin/{nit}")
def detalle_reciclador_admin(
    nit: int,
    _: dict = Depends(require_colaborador),
    service: RecicladorService = Depends(get_reciclador_service),
):
    return service.obtener_detalle_admin(nit)
