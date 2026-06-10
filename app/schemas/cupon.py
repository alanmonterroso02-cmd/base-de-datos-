from pydantic import BaseModel
from uuid import UUID


class CuponCreate(BaseModel):
    codigo: str
    premio_id: UUID
    reciclador_nit: int


class CuponOut(BaseModel):
    id: UUID
    codigo: str
    premio_id: UUID
    reciclador_nit: int
    fecha_emision: str
    fecha_expiracion: str
    esta_usado: bool
    premio_nombre: str
    premio_imagen: str | None = None
