from sqlmodel import Session
from fastapi import APIRouter, Depends

from database import get_session
from app.service.categoria_reciclaje_service import CategoriaReciclajeService
from app.util.auth import get_current_reciclador

categoria_router = APIRouter(
    prefix="/categorias-reciclaje", tags=["Categorías Reciclaje"]
)


@categoria_router.get("/formulario")
def obtener_categorias_formulario(
    _: dict = Depends(get_current_reciclador), session: Session = Depends(get_session)
):
    service = CategoriaReciclajeService(session)

    categorias = service.obtener_para_formulario()

    return [
        {"id": categoria.id, "nombre": categoria.nombre} for categoria in categorias
    ]
