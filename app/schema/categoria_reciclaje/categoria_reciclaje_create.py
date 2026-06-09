from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class CategoriaReciclajeCreate(BaseModel):
    nombre: str
    puntos_por_gramo: Decimal
    imagen: Optional[str] = None
