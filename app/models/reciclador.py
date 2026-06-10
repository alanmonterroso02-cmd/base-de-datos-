from decimal import Decimal
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.cupon import Cupon


class Reciclador(SQLModel, table=True):
    __tablename__ = "recicladores"

    nit: int = Field(primary_key=True)
    nombre_completo: str
    puntos: Decimal = Field(default=0, decimal_places=2, max_digits=12)

    cupones: List["Cupon"] = Relationship(back_populates="reciclador")
