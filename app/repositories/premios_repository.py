from sqlmodel import Session, select

from app.models.premio import Premio
from app.repositories.base import BaseRepository


class PremioRepository(BaseRepository[Premio]):
    def __init__(self, session: Session):
        super().__init__(session, Premio)

    def find_all_ordered(self) -> list[Premio]:
        return self.session.exec(select(Premio).order_by(Premio.nombre)).all()

    def find_active(self) -> list[Premio]:
        return self.session.exec(
            select(
                Premio.id,
                Premio.nombre,
                Premio.imagen,
                Premio.descripcion,
                Premio.costo_puntos,
                Premio.stock,
            ).where(Premio.activa)
        ).all()
