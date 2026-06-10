from decimal import Decimal
from uuid import UUID, uuid4
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.cupon import Cupon


class Premio(SQLModel, table=True):
    __tablename__ = "premios"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    costo_puntos: Decimal = Field(decimal_places=2, max_digits=12)
    stock: int
    activa: bool = Field(default=True)

    cupones: List["Cupon"] = Relationship(back_populates="premio")
