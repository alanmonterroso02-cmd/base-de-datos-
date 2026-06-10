from uuid import UUID, uuid4
from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.premio import Premio
    from app.models.reciclador import Reciclador


class Cupon(SQLModel, table=True):
    __tablename__ = "cupones"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    codigo: str = Field(unique=True, index=True)

    premio_id: UUID = Field(foreign_key="premios.id")
    reciclador_nit: int = Field(foreign_key="recicladores.nit")

    fecha_emision: date
    fecha_expiracion: date
    esta_usado: bool = Field(default=False)

    premio: "Premio" = Relationship(back_populates="cupones")
    reciclador: "Reciclador" = Relationship(back_populates="cupones")
