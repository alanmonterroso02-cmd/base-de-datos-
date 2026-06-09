from decimal import Decimal
from uuid import UUID, uuid4
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class PremioModel(SQLModel, table=True):
    __tablename__ = "premios"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    costo_puntos: Decimal = Field(decimal_places=2, max_digits=12)
    stock: int
    activa: bool = Field(default=True)

    cupones: List["CuponModel"] = Relationship(back_populates="premio")
