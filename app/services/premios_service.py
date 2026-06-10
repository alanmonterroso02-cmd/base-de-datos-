from datetime import date, timedelta
from uuid import uuid4
from fastapi import HTTPException, status

from app.repositories.premios_repository import PremioRepository
from app.repositories.recicladores_repository import RecicladorRepository
from app.models.premio import Premio
from app.models.cupon import Cupon
from app.models.movimiento_puntos import MovimientoPuntos
from app.schemas.premio import PremioCreate, PremioUpdate


class PremiosService:
    def __init__(
        self,
        premio_repo: PremioRepository,
        reciclador_repo: RecicladorRepository,
    ):
        self.premio_repo = premio_repo
        self.reciclador_repo = reciclador_repo

    def obtener_premio(self, premio_id: str) -> Premio | None:
        return self.premio_repo.get(premio_id)

    def crear_premio(self, premio_data: PremioCreate):
        nuevo = Premio.model_validate(premio_data)
        return self.premio_repo.add(nuevo)

    def actualizar_premio(self, premio_id: str, premio_data: PremioUpdate):
        premio = self.obtener_premio(premio_id)
        if not premio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Premio no encontrado",
            )

        update_data = premio_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(premio, key, value)

        return self.premio_repo.update(premio)

    def toggle_activo(self, premio_id: str):
        premio = self.obtener_premio(premio_id)
        if not premio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Premio no encontrado",
            )
        premio.activa = not premio.activa
        return self.premio_repo.update(premio)

    def agregar_stock(self, premio_id: str, cantidad: int):
        premio = self.obtener_premio(premio_id)
        if not premio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Premio no encontrado",
            )
        premio.stock += cantidad
        return self.premio_repo.update(premio)

    def canjear_premio(self, premio_id: str, reciclador_nit: int):
        reciclador = self.reciclador_repo.find_by_nit(reciclador_nit)
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
            raise HTTPException(
                status_code=400,
                detail="Puntos insuficientes para canjear este premio",
            )

        reciclador.puntos -= premio.costo_puntos
        premio.stock -= 1

        codigo = str(uuid4()).replace("-", "").upper()[:8]
        cupon = Cupon(
            codigo=codigo,
            premio_id=premio.id,
            reciclador_nit=reciclador.nit,
            fecha_emision=date.today(),
            fecha_expiracion=date.today() + timedelta(days=30),
        )

        movimiento = MovimientoPuntos(
            reciclador_nit=reciclador_nit,
            puntos=-premio.costo_puntos,
            motivo=f"Canje de {premio.nombre}",
        )

        self.premio_repo.session.add(reciclador)
        self.premio_repo.session.add(premio)
        self.premio_repo.session.add(cupon)
        self.premio_repo.session.add(movimiento)
        self.premio_repo.session.commit()
        self.premio_repo.session.refresh(cupon)

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

    def listar_premios_admin(self):
        rows = self.premio_repo.find_all_ordered()
        return [
            {
                "id": str(r.id),
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "imagen": r.imagen,
                "costo_puntos": float(r.costo_puntos),
                "stock": r.stock,
                "activa": r.activa,
            }
            for r in rows
        ]

    def listar_premios(self):
        rows = self.premio_repo.find_active()
        return [
            {
                "id": str(r.id),
                "nombre": r.nombre,
                "imagen": r.imagen,
                "descripcion": r.descripcion,
                "costo_puntos": float(r.costo_puntos),
                "stock": r.stock,
            }
            for r in rows
        ]
