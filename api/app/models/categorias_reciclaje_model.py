from uuid import UUID,uuid4
from decimal import Decimal

from sqlmodel import SQLModel, Field


class CategoriaReciclajeModel(SQLModel, table=True):
    __tablename__ = "categorias_reciclaje"


    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )
    nombre: str = Field(unique=True)
    puntos_por_gramo: Decimal = Field(
        default=0,
        decimal_places=2,
        max_digits=10
    )
    activa: bool = Field(default=True)