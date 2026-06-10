from sqlmodel import Session, select
from uuid import UUID

from app.models.usuario import Usuario
from app.repositories.base import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(session, Usuario)

    def get_all(self) -> list[Usuario]:
        return self.session.exec(
            select(Usuario).order_by(Usuario.nombre_completo)
        ).all()

    def find_by_correo(self, correo: str) -> Usuario | None:
        return self.session.exec(
            select(Usuario).where(Usuario.correo == correo, Usuario.activo == True)
        ).first()

    def find_by_id(self, usuario_id: str) -> Usuario | None:
        return self.session.get(Usuario, UUID(usuario_id))
