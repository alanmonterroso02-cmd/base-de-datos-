from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import Optional

class PremioOut(BaseModel):
    id: UUID
    nombre: str
    imagen: Optional[str] = None
    descripcion: Optional[str] = None
    costo_puntos: Decimal
    stock: int
