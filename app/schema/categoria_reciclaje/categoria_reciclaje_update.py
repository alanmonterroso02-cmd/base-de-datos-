from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class CategoriaReciclajeUpdate(BaseModel):
    nombre: Optional[str] = None
    puntos_por_gramo: Optional[Decimal] = None
    imagen: Optional[str] = None
