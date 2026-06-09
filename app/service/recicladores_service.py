from decimal import Decimal
from fastapi import HTTPException
from sqlmodel import Session, select

from ..util.jwt_manager import create_token
from app.models.recicladores_model import RecicladoresModel
from app.models.categorias_reciclaje_model import CategoriaReciclajeModel
from app.models.movimiento_puntos_model import MovimientoPuntos
from app.models.cupon_model import CuponModel
from app.models.premio_model import PremioModel
from app.schema.reciclador import RecicladorLoginResponse, PuntosAgregarResponse, MovimientoPuntosOut, RecicladorPerfilOut


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

        return RecicladorLoginResponse(token=token)

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

        return PuntosAgregarResponse(
            puntos_agregados=float(puntos),
            total_actual=float(reciclador.puntos),
        )
    def ver_perfil(self, nit: int):
        reciclador = self.session.get(RecicladoresModel, nit)
        if not reciclador:
            raise HTTPException(status_code=404, detail="Reciclador no encontrado")

        return RecicladorPerfilOut(
            nit=reciclador.nit,
            nombre_completo=reciclador.nombre_completo,
            puntos=float(reciclador.puntos),
        )

    def ver_historial_puntos(self, nit: int):
        rows = self.session.exec(
            select(MovimientoPuntos).where(MovimientoPuntos.resiclador_nit == nit)
        ).all()

        return [
            MovimientoPuntosOut(
                id=str(row.id),
                resiclador_nit=row.resiclador_nit,
                puntos=float(row.puntos),
                motivo=row.motivo,
                fecha=row.fecha,
            )
            for row in rows
        ]

    def listar_cupones(self, nit: int):
        rows = self.session.exec(
            select(CuponModel, PremioModel)
            .join(PremioModel, CuponModel.premio_id == PremioModel.id)
            .where(CuponModel.reciclador_nit == nit)
            .order_by(CuponModel.fecha_emision.desc())
        ).all()

        return [
            {
                "id": str(cupon.id),
                "codigo": cupon.codigo,
                "premio_id": str(cupon.premio_id),
                "premio_nombre": premio.nombre,
                "premio_imagen": premio.imagen,
                "fecha_emision": cupon.fecha_emision.isoformat(),
                "fecha_expiracion": cupon.fecha_expiracion.isoformat(),
                "esta_usado": cupon.esta_usado,
            }
            for cupon, premio in rows
        ]
