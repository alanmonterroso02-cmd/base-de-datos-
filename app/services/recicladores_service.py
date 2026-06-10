from decimal import Decimal
from fastapi import HTTPException

from app.repositories.recicladores_repository import RecicladorRepository
from app.repositories.categorias_repository import CategoriaReciclajeRepository
from app.repositories.cupones_repository import CuponRepository
from app.utils.jwt_manager import create_token
from app.models.reciclador import Reciclador
from app.schemas.reciclador import (
    RecicladorLoginResponse,
    PuntosAgregarResponse,
    MovimientoPuntosOut,
    RecicladorPerfilOut,
    RecicladorAdminOut,
    RecicladorAdminDetailOut,
    RecicladorCreate,
    MovimientoPuntosAdminOut,
    CuponAdminOut,
)


class RecicladorService:
    def __init__(
        self,
        reciclador_repo: RecicladorRepository,
        categoria_repo: CategoriaReciclajeRepository,
        cupon_repo: CuponRepository,
    ):
        self.reciclador_repo = reciclador_repo
        self.categoria_repo = categoria_repo
        self.cupon_repo = cupon_repo

    def login(self, nit: int):
        reciclador = self.reciclador_repo.find_by_nit(nit)
        if not reciclador:
            return None
        token = create_token({"nit": reciclador.nit})
        return RecicladorLoginResponse(token=token)

    def crear_reciclador(self, data: RecicladorCreate) -> RecicladorAdminOut:
        existe = self.reciclador_repo.find_by_nit(data.nit)
        if existe:
            raise HTTPException(
                status_code=400, detail=f"Ya existe un reciclador con NIT {data.nit}"
            )
        reciclador = Reciclador(nit=data.nit, nombre_completo=data.nombre_completo)
        self.reciclador_repo.add(reciclador)
        return RecicladorAdminOut(
            nit=reciclador.nit,
            nombre_completo=reciclador.nombre_completo,
            puntos=float(reciclador.puntos),
        )

    def crear_recicladores_masivo(self, items: list[RecicladorCreate]) -> dict:
        creados = []
        errores = []
        for data in items:
            existe = self.reciclador_repo.find_by_nit(data.nit)
            if existe:
                errores.append(f"NIT {data.nit} ya existe")
                continue
            reciclador = Reciclador(nit=data.nit, nombre_completo=data.nombre_completo)
            self.reciclador_repo.session.add(reciclador)
            self.reciclador_repo.session.flush()
            creados.append(
                RecicladorAdminOut(
                    nit=reciclador.nit,
                    nombre_completo=reciclador.nombre_completo,
                    puntos=float(reciclador.puntos),
                )
            )
        self.reciclador_repo.session.commit()
        return {"creados": creados, "errores": errores}

    def agregar_puntos(self, nit: int, material):
        reciclador = self.reciclador_repo.find_by_nit(nit)
        if not reciclador:
            raise HTTPException(status_code=404, detail="Reciclador no encontrado")

        categoria = self.categoria_repo.find_by_id(material.categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

        puntos = Decimal(str(material.gramos)) * categoria.puntos_por_gramo
        reciclador.puntos += puntos

        from app.models.movimiento_puntos import MovimientoPuntos

        movimiento = MovimientoPuntos(
            reciclador_nit=nit, puntos=puntos, motivo=f"Reciclaje {categoria.nombre}"
        )

        self.reciclador_repo.session.add(movimiento)
        self.reciclador_repo.update(reciclador)

        return PuntosAgregarResponse(
            puntos_agregados=float(puntos),
            total_actual=float(reciclador.puntos),
        )

    def ver_perfil(self, nit: int):
        reciclador = self.reciclador_repo.find_by_nit(nit)
        if not reciclador:
            raise HTTPException(status_code=404, detail="Reciclador no encontrado")
        return RecicladorPerfilOut(
            nit=reciclador.nit,
            nombre_completo=reciclador.nombre_completo,
            puntos=float(reciclador.puntos),
        )

    def ver_historial_puntos(self, nit: int):
        rows = self.reciclador_repo.find_movimientos_by_nit(nit)
        return [
            MovimientoPuntosOut(
                id=str(r.id),
                reciclador_nit=r.reciclador_nit,
                puntos=float(r.puntos),
                motivo=r.motivo,
                fecha=r.fecha,
            )
            for r in rows
        ]

    def listar_cupones(self, nit: int):
        rows = self.cupon_repo.find_by_reciclador_with_premio(nit)
        return [
            {
                "id": str(c.id),
                "codigo": c.codigo,
                "premio_id": str(c.premio_id),
                "premio_nombre": p.nombre,
                "premio_imagen": p.imagen,
                "fecha_emision": c.fecha_emision.isoformat(),
                "fecha_expiracion": c.fecha_expiracion.isoformat(),
                "esta_usado": c.esta_usado,
            }
            for c, p in rows
        ]

    def listar_todos(self) -> list[RecicladorAdminOut]:
        rows = self.reciclador_repo.get_all()
        return [
            RecicladorAdminOut(
                nit=r.nit,
                nombre_completo=r.nombre_completo,
                puntos=float(r.puntos),
            )
            for r in rows
        ]

    def obtener_detalle_admin(self, nit: int) -> RecicladorAdminDetailOut:
        reciclador = self.reciclador_repo.find_by_nit(nit)
        if not reciclador:
            raise HTTPException(status_code=404, detail="Reciclador no encontrado")

        try:
            historial = self.ver_historial_puntos(nit)
            historial_out = [
                MovimientoPuntosAdminOut(
                    id=h.id,
                    puntos=h.puntos,
                    motivo=h.motivo,
                    fecha=h.fecha,
                )
                for h in historial
            ]
        except Exception:
            historial_out = []

        try:
            cupones_rows = self.cupon_repo.find_by_reciclador_with_premio(nit)
            cupones_out = [
                CuponAdminOut(
                    id=str(c.id),
                    codigo=c.codigo,
                    premio_nombre=p.nombre,
                    premio_imagen=p.imagen,
                    fecha_emision=c.fecha_emision.isoformat(),
                    fecha_expiracion=c.fecha_expiracion.isoformat(),
                    esta_usado=c.esta_usado,
                )
                for c, p in cupones_rows
            ]
        except Exception:
            cupones_out = []

        return RecicladorAdminDetailOut(
            nit=reciclador.nit,
            nombre_completo=reciclador.nombre_completo,
            puntos=float(reciclador.puntos),
            historial=historial_out,
            cupones=cupones_out,
        )
