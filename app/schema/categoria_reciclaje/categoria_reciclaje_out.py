from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from decimal import Decimal

class CategoriaReciclajeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nombre: str