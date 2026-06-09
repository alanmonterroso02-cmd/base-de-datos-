from datetime import date, timedelta
from uuid import uuid4

from sqlmodel import Session, select
from fastapi import HTTPException, status
from uuid import UUID

from app.models.premio_model import PremioModel
from app.models.recicladores_model import RecicladoresModel
from app.models.cupon_model import CuponModel
from app.models.movimiento_puntos_model import MovimientoPuntos
from app.schema.premio import PremioCreate, PremioUpdate

class PremiosService:
    def __init__(self, session: Session):
        self.session = session

    def obtener_premio(self, premio_id: str) -> PremioModel | None:
        return self.session.get(PremioModel, premio_id)

    def crear_premio(self, premio_data: PremioCreate):
        nuevo_premio = PremioModel.model_validate(premio_data)
        self.session.add(nuevo_premio)
        self.session.commit()
        self.session.refresh(nuevo_premio)
        return nuevo_premio

    def actualizar_premio(self, premio_id: str, premio_data: PremioUpdate):
        premio = self.obtener_premio(premio_id)
        if not premio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Premio no encontrado"
            )

        update_data = premio_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(premio, key, value)

        self.session.add(premio)
        self.session.commit()
        self.session.refresh(premio)
        return premio

    def agregar_stock(self, premio_id: str, cantidad: int):
        premio = self.obtener_premio(premio_id)
        if not premio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Premio no encontrado"
            )

        premio.stock += cantidad
        self.session.add(premio)
        self.session.commit()
        self.session.refresh(premio)
        return premio

    def canjear_premio(self, premio_id: str, reciclador_nit: int):
        reciclador = self.session.get(RecicladoresModel, reciclador_nit)
        if not reciclador:
            raise HTTPException(status_code=404, detail="Reciclador no encontrado")

        premio = self.obtener_premio(premio_id)
        if not premio:
            raise HTTPException(status_code=404, detail="Premio no encontrado")

        if not premio.activa:
            raise HTTPException(status_code=400, detail="Premio no disponible")

        if premio.stock < 1:
            raise HTTPException(status_code=400, detail="Premio sin stock disponible")

        if reciclador.puntos < premio.costo_puntos:
            raise HTTPException(status_code=400, detail="Puntos insuficientes para canjear este premio")

        reciclador.puntos -= premio.costo_puntos
        premio.stock -= 1

        codigo = str(uuid4()).replace("-", "").upper()[:8]

        cupon = CuponModel(
            codigo=codigo,
            premio_id=premio.id,
            reciclador_nit=reciclador.nit,
            fecha_emision=date.today(),
            fecha_expiracion=date.today() + timedelta(days=30),
        )

        movimiento = MovimientoPuntos(
            resiclador_nit=reciclador_nit,
            puntos=-premio.costo_puntos,
            motivo=f"Canje de {premio.nombre}",
        )

        self.session.add(reciclador)
        self.session.add(premio)
        self.session.add(cupon)
        self.session.add(movimiento)
        self.session.commit()
        self.session.refresh(cupon)

        return {
            "cupon": {
                "id": str(cupon.id),
                "codigo": cupon.codigo,
                "fecha_emision": cupon.fecha_emision.isoformat(),
                "fecha_expiracion": cupon.fecha_expiracion.isoformat(),
            },
            "puntos_restantes": float(reciclador.puntos),
            "mensaje": f"Canje exitoso de {premio.nombre}",
        }

    def listar_premios(self):
        rows = self.session.exec(
            select(
                PremioModel.id,
                PremioModel.nombre,
                PremioModel.imagen,
                PremioModel.descripcion,
                PremioModel.costo_puntos,
                PremioModel.stock
            ).where(PremioModel.activa)
        ).all()

        return [
            {
                "id": row.id,
                "nombre": row.nombre,
                "imagen": row.imagen,
                "descripcion": row.descripcion,
                "costo_puntos": row.costo_puntos,
                "stock": row.stock
            }
            for row in rows
        ]
