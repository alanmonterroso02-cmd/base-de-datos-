from pydantic import BaseModel
from datetime import datetime

class MovimientoPuntosOut(BaseModel):
    id: str
    resiclador_nit: int
    puntos: float
    motivo: str
    fecha: datetime
