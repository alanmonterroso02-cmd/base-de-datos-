from sqlmodel import Session, select
from uuid import UUID

from app.models.categoria_reciclaje import CategoriaReciclaje
from app.repositories.base import BaseRepository


class CategoriaReciclajeRepository(BaseRepository[CategoriaReciclaje]):
    def __init__(self, session: Session):
        super().__init__(session, CategoriaReciclaje)

    def get_all(self) -> list[CategoriaReciclaje]:
        return self.session.exec(
            select(CategoriaReciclaje).order_by(CategoriaReciclaje.nombre)
        ).all()

    def find_by_id(self, categoria_id: UUID) -> CategoriaReciclaje | None:
        return self.session.get(CategoriaReciclaje, categoria_id)
