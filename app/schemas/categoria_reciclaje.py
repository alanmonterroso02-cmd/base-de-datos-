from pydantic import BaseModel, ConfigDict
from uuid import UUID
from decimal import Decimal
from typing import Optional


class CategoriaReciclajeCreate(BaseModel):
    nombre: str
    puntos_por_gramo: float


class CategoriaReciclajeUpdate(BaseModel):
    nombre: Optional[str] = None
    puntos_por_gramo: Optional[float] = None


class CategoriaReciclajeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nombre: str
    puntos_por_gramo: Decimal
