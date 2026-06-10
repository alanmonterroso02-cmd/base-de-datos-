from fastapi import APIRouter, Depends, status, HTTPException, Form
from sqlmodel import Session
from uuid import UUID
from typing import Optional

from app.core.database import get_session
from app.repositories.categorias_repository import CategoriaReciclajeRepository
from app.services.categoria_reciclaje_service import CategoriaReciclajeService
from app.schemas.categoria_reciclaje import (
    CategoriaReciclajeCreate,
    CategoriaReciclajeUpdate,
)
from app.utils.auth import require_colaborador

categoria_router = APIRouter(
    prefix="/categorias-reciclaje", tags=["Categorías Reciclaje"]
)


def get_service(session: Session = Depends(get_session)):
    repo = CategoriaReciclajeRepository(session)
    return CategoriaReciclajeService(repo)


@categoria_router.get("/admin/list")
def listar_categorias(
    _: dict = Depends(require_colaborador),
    service: CategoriaReciclajeService = Depends(get_service),
):
    return service.listar_categorias()


@categoria_router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    _: dict = Depends(require_colaborador),
    nombre: str = Form(...),
    puntos_por_gramo: float = Form(...),
    service: CategoriaReciclajeService = Depends(get_service),
):
    data = CategoriaReciclajeCreate(
        nombre=nombre,
        puntos_por_gramo=puntos_por_gramo,
    )
    return service.crear_categoria(data)


@categoria_router.put("/{categoria_id}")
async def actualizar_categoria(
    categoria_id: UUID,
    _: dict = Depends(require_colaborador),
    nombre: Optional[str] = Form(None),
    puntos_por_gramo: Optional[float] = Form(None),
    service: CategoriaReciclajeService = Depends(get_service),
):
    categoria_actual = service.obtener_categoria(categoria_id)
    if not categoria_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )

    update_dict = {}
    if nombre is not None:
        update_dict["nombre"] = nombre
    if puntos_por_gramo is not None:
        update_dict["puntos_por_gramo"] = puntos_por_gramo

    data = CategoriaReciclajeUpdate(**update_dict)
    return service.actualizar_categoria(categoria_id, data)
