from sqlmodel import Session
from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from uuid import UUID
from typing import Optional

from database import get_session
from app.service.categoria_reciclaje_service import CategoriaReciclajeService
from app.schema.categoria_reciclaje import CategoriaReciclajeCreate, CategoriaReciclajeUpdate
from app.util.auth import require_colaborador, get_current_reciclador
from app.util.file_manager import FileManager

categoria_router = APIRouter(
    prefix="/categorias-reciclaje", tags=["Categorías Reciclaje"]
)


def get_service(session: Session = Depends(get_session)):
    return CategoriaReciclajeService(session)


@categoria_router.get("/formulario")
def obtener_categorias_formulario(
    _: dict = Depends(get_current_reciclador),
    service: CategoriaReciclajeService = Depends(get_service),
):
    return service.obtener_para_formulario()


@categoria_router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    _: dict = Depends(require_colaborador),
    nombre: str = Form(...),
    puntos_por_gramo: float = Form(...),
    imagen: UploadFile = File(None),
    service: CategoriaReciclajeService = Depends(get_service),
):
    imagen_url = None
    if imagen:
        imagen_url = FileManager.save_upload_file(imagen, subdir="categorias")

    data = CategoriaReciclajeCreate(
        nombre=nombre,
        puntos_por_gramo=puntos_por_gramo,
        imagen=imagen_url,
    )

    return service.crear_categoria(data)


@categoria_router.put("/{categoria_id}")
async def actualizar_categoria(
    categoria_id: UUID,
    _: dict = Depends(require_colaborador),
    nombre: Optional[str] = Form(None),
    puntos_por_gramo: Optional[float] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    service: CategoriaReciclajeService = Depends(get_service),
):
    categoria_actual = service.obtener_categoria(categoria_id)
    if not categoria_actual:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")

    nueva_imagen_url = None
    if imagen:
        nueva_imagen_url = FileManager.save_upload_file(imagen, subdir="categorias")
        if categoria_actual.imagen:
            FileManager.delete_file(categoria_actual.imagen)

    update_dict = {}
    if nombre is not None:
        update_dict["nombre"] = nombre
    if puntos_por_gramo is not None:
        update_dict["puntos_por_gramo"] = puntos_por_gramo
    if nueva_imagen_url:
        update_dict["imagen"] = nueva_imagen_url

    data = CategoriaReciclajeUpdate(**update_dict)
    return service.actualizar_categoria(categoria_id, data)
