from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PremioCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    costo_puntos: Decimal
    stock: int
