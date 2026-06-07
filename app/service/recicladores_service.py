from decimal import Decimal
from fastapi import HTTPException
from sqlmodel import Session, select

from ..util.jwt_manager import create_token
from app.models.recicladores_model import RecicladoresModel
from app.models.categorias_reciclaje_model import CategoriaReciclajeModel
from app.models.movimiento_puntos_model import MovimientoPuntos


class RecicladorService:
    def __init__(self, session: Session):
        self.session = session

    def login(self, nit: int):

        reciclador = self.session.exec(
            select(RecicladoresModel).where(RecicladoresModel.nit == nit)
        ).first()

        if not reciclador:
            return None

        token = create_token({"nit": reciclador.nit})

        return {"token": token}

    def agregar_puntos(self, nit: int, material):
        reciclador = self.session.get(RecicladoresModel, nit)

        if not reciclador:
            raise HTTPException(status_code=404, detail="Reciclador no encontrado")

        categoria = self.session.get(CategoriaReciclajeModel, material.categoria_id)

        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

        puntos = Decimal(str(material.gramos)) * categoria.puntos_por_gramo

        reciclador.puntos += puntos

        movimiento = MovimientoPuntos(
            resiclador_nit=nit, puntos=puntos, motivo=f"Reciclaje {categoria.nombre}"
        )

        self.session.add(movimiento)
        self.session.add(reciclador)

        self.session.commit()
        self.session.refresh(reciclador)

        return {
            "puntos_agregados": float(puntos),
            "total_actual": float(reciclador.puntos),
        }
