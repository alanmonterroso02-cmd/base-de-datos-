from pydantic import BaseModel

class PremioStockUpdate(BaseModel):
    cantidad: int
