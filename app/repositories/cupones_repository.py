from sqlmodel import Session, select

from app.models.cupon import Cupon
from app.models.premio import Premio
from app.repositories.base import BaseRepository


class CuponRepository(BaseRepository[Cupon]):
    def __init__(self, session: Session):
        super().__init__(session, Cupon)

    def find_by_codigo(self, codigo: str) -> Cupon | None:
        return self.session.exec(select(Cupon).where(Cupon.codigo == codigo)).first()

    def find_by_reciclador_with_premio(self, nit: int) -> list[tuple[Cupon, Premio]]:
        return self.session.exec(
            select(Cupon, Premio)
            .join(Premio, Cupon.premio_id == Premio.id)
            .where(Cupon.reciclador_nit == nit)
            .order_by(Cupon.fecha_emision.desc())
        ).all()
