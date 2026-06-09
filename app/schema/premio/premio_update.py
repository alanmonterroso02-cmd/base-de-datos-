from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PremioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    costo_puntos: Optional[Decimal] = None
