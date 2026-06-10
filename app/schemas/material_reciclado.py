from pydantic import BaseModel, Field
from uuid import UUID


class MaterialRecicladoSchema(BaseModel):
    categoria_id: UUID
    gramos: int = Field(gt=0, le=50000)
