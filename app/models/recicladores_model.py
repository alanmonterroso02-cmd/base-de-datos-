from decimal import Decimal
from typing import List
from sqlmodel import SQLModel, Field, Relationship

class RecicladoresModel(SQLModel, table=True):
    __tablename__ = "resicladores"

    nit: int = Field(primary_key=True)

    nombre_completo: str

    puntos: Decimal = Field(default=0, decimal_places=2, max_digits=12)

    cupones: List["CuponModel"] = Relationship(back_populates="reciclador")
