from uuid import UUID, uuid4
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class CuponModel(SQLModel, table=True):
    __tablename__ = "cupones"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    codigo: str = Field(unique=True, index=True)

    premio_id: UUID = Field(foreign_key="premios.id")
    reciclador_nit: int = Field(foreign_key="resicladores.nit")

    fecha_emision: date
    fecha_expiracion: date
    esta_usado: bool = Field(default=False)

    premio: "PremioModel" = Relationship(back_populates="cupones")
    reciclador: "RecicladoresModel" = Relationship(back_populates="cupones")
