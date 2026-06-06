from sqlmodel import select, Session
from fastapi import HTTPException, status

from ..models.user_model import UsuariosModel


class UserValidator:
    def __init__(self, session: Session):
        self.session = session

    def validate_email_exists(self, correo: str) -> None:
        existing = self.session.exec(
            select(UsuariosModel).where(UsuariosModel.correo == correo)
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya está registrado.",
            )

    def validate_name_exists(self, nombre: str) -> None:
        existing = self.session.exec(
            select(UsuariosModel).where(UsuariosModel.nombre_completo == nombre)
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre ya está registrado.",
            )