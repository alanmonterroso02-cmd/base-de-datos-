from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional


class RecicladorLoginResponse(BaseModel):
    token: str


class PuntosAgregarResponse(BaseModel):
    puntos_agregados: float
    total_actual: float


class MovimientoPuntosOut(BaseModel):
    id: str
    reciclador_nit: int
    puntos: float
    motivo: str
    fecha: datetime


class RecicladorPerfilOut(BaseModel):
    nit: int
    nombre_completo: str
    puntos: float


class RecicladorAdminOut(BaseModel):
    nit: int
    nombre_completo: str
    puntos: float


class MovimientoPuntosAdminOut(BaseModel):
    id: str
    puntos: float
    motivo: str
    fecha: datetime


class CuponAdminOut(BaseModel):
    id: str
    codigo: str
    premio_nombre: str
    premio_imagen: Optional[str] = None
    fecha_emision: str
    fecha_expiracion: str
    esta_usado: bool


class RecicladorAdminDetailOut(BaseModel):
    nit: int
    nombre_completo: str
    puntos: float
    historial: list[MovimientoPuntosAdminOut]
    cupones: list[CuponAdminOut]


class RecicladorCreate(BaseModel):
    nit: int
    nombre_completo: str
