from pydantic import BaseModel

class PuntosAgregarResponse(BaseModel):
    puntos_agregados: float
    total_actual: float
