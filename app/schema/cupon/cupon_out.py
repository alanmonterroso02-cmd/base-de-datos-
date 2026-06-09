from pydantic import BaseModel
from uuid import UUID
from datetime import date

class CuponOut(BaseModel):
    id: UUID
    codigo: str
    premio_id: UUID
    reciclador_nit: int
    fecha_emision: date
    fecha_expiracion: date
    esta_usado: bool
