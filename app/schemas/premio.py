from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class PremioCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    costo_puntos: float
    stock: int


class PremioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    costo_puntos: Optional[float] = None
    imagen: Optional[str] = None


class PremioStockUpdate(BaseModel):
    cantidad: int


class PremioOut(BaseModel):
    id: UUID
    nombre: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    costo_puntos: float
    stock: int
    activa: bool
