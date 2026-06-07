from decimal import Decimal
from sqlmodel import SQLModel, Field


class RecicladoresModel(SQLModel, table=True):
    __tablename__ = "resicladores"

    nit: int = Field(primary_key=True)

    nombre_completo: str

    puntos: Decimal = Field(default=0, decimal_places=2, max_digits=12)
