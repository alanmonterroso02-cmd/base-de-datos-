from sqlmodel import select, Session
from fastapi import HTTPException, status

from ..models.user_model import UsuariosModel


class UserValidator:
    def __init__(self, session: Session):
        self.session = session

    def validate_uniqueness(self, correo: str, nombre: str) -> None:
        existing = self.session.exec(
            select(UsuariosModel).where(
                (UsuariosModel.correo == correo)
                | (UsuariosModel.nombre_completo == nombre)
            )
        ).first()

        if existing:
            if existing.correo == correo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo ya está registrado.",
                )
            if existing.nombre_completo == nombre:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre ya está registrado.",
                )
