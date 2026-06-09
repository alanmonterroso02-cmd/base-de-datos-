from pydantic import BaseModel
from decimal import Decimal


class RecicladorPerfilOut(BaseModel):
    nit: int
    nombre_completo: str
    puntos: float
