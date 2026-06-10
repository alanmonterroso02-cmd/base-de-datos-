from sqlmodel import Session, select

from app.models.reciclador import Reciclador
from app.models.movimiento_puntos import MovimientoPuntos
from app.repositories.base import BaseRepository


class RecicladorRepository(BaseRepository[Reciclador]):
    def __init__(self, session: Session):
        super().__init__(session, Reciclador)

    def find_by_nit(self, nit: int) -> Reciclador | None:
        return self.session.get(Reciclador, nit)

    def find_movimientos_by_nit(self, nit: int) -> list[MovimientoPuntos]:
        return self.session.exec(
            select(MovimientoPuntos).where(MovimientoPuntos.reciclador_nit == nit)
        ).all()
