from uuid import UUID
from pydantic import BaseModel, Field


class MaterialRecicladoSchema(BaseModel):
    categoria_id: UUID
    gramos: float = Field(
        gt=0,
        le=50000
    )