from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlmodel import Session
from uuid import UUID
from typing import Optional

from database import get_session
from app.service.premios_service import PremiosService
from app.schema.premio import PremioCreate, PremioUpdate, PremioStockUpdate
from app.util.file_manager import FileManager
from app.util.auth import get_current_reciclador, require_colaborador

router = APIRouter(prefix="/premios", tags=["Premios"])

def get_premios_service(session: Session = Depends(get_session)):
    return PremiosService(session)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_premio(
    _: dict = Depends(require_colaborador),
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    costo_puntos: float = Form(...),
    stock: int = Form(...),
    imagen: UploadFile = File(...),
    service: PremiosService = Depends(get_premios_service),
):
    imagen_url = FileManager.save_upload_file(imagen)

    premio_data = PremioCreate(
        nombre=nombre,
        descripcion=descripcion,
        imagen=imagen_url,
        costo_puntos=costo_puntos,
        stock=stock,
    )

    return service.crear_premio(premio_data)

@router.put("/{premio_id}")
async def actualizar_premio(
    premio_id: UUID,
    _: dict = Depends(require_colaborador),
    nombre: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    costo_puntos: Optional[float] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    service: PremiosService = Depends(get_premios_service),
):
    premio_actual = service.obtener_premio(premio_id)
    if not premio_actual:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Premio no encontrado")

    nueva_imagen_url = None
    if imagen:
        nueva_imagen_url = FileManager.save_upload_file(imagen)
        FileManager.delete_file(premio_actual.imagen)

    update_dict = {}
    if nombre is not None: update_dict["nombre"] = nombre
    if descripcion is not None: update_dict["descripcion"] = descripcion
    if costo_puntos is not None: update_dict["costo_puntos"] = costo_puntos
    if nueva_imagen_url: update_dict["imagen"] = nueva_imagen_url

    premio_update = PremioUpdate(**update_dict)
    return service.actualizar_premio(premio_id, premio_update)

@router.patch("/{premio_id}/stock")
async def aumentar_stock(
    premio_id: UUID,
    stock_data: PremioStockUpdate,
    _: dict = Depends(require_colaborador),
    service: PremiosService = Depends(get_premios_service),
):
    """Aumenta el stock de un premio específico."""
    return service.agregar_stock(premio_id, stock_data.cantidad)

@router.post("/{premio_id}/canjear")
async def canjear_premio(
    premio_id: UUID,
    reciclador=Depends(get_current_reciclador),
    service: PremiosService = Depends(get_premios_service),
):
    return service.canjear_premio(premio_id, reciclador["nit"])

@router.get("/form", response_model=list)
async def listar_premios(
    _: dict = Depends(get_current_reciclador),
    service: PremiosService = Depends(get_premios_service),
):
    return service.listar_premios()
