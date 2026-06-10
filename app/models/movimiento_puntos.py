from decimal import Decimal
from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class MovimientoPuntos(SQLModel, table=True):
    __tablename__ = "movimientos_puntos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    reciclador_nit: int = Field(foreign_key="recicladores.nit", index=True)
    puntos: Decimal = Field(default=0, decimal_places=2, max_digits=12)
    motivo: str
    fecha: datetime = Field(default_factory=datetime.now)
