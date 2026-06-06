import secrets
from sqlmodel import Session, select
from fastapi import Depends, HTTPException

from database import get_session
from ..models.user_model import UsuariosModel, RolEnum
from ..schemas.create_user import CreateUserRequestSchema
from ..schemas.login_user import LoginRequestSchema
from ..util.password_service import PasswordService
from ..util.jwt_service import JWTService
from ..validators.user_validator import UserValidator


class UsuariosAutenticacionService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.validator = UserValidator(self.session)

    async def create(self, data: CreateUserRequestSchema) -> dict:
        self.validator.validate_email_exists(data.correo)
        self.validator.validate_name_exists(data.nombre_completo)

        raw_pin = str(secrets.randbelow(900_000_000_000) + 100_000_000_000)

        user = UsuariosModel(
            nombre_completo=data.nombre_completo,
            correo=data.correo,        
            pin=PasswordService.hash(raw_pin),
            rol=RolEnum.Usuario,
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return {
            "id": user.id,
            "correo": user.correo,        
            "context": {
                "nombre": user.nombre_completo,
                "token": user.id,
                "pin": raw_pin,
            },
        }

    async def login(self, data: LoginRequestSchema) -> dict:
        user = self.session.exec(
            select(UsuariosModel).where(UsuariosModel.id == data.token)
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not PasswordService.verify(data.pin, user.pin):
            raise HTTPException(status_code=401, detail="PIN incorrecto")

        access_token = JWTService.create_token(
            user_id=user.id,
            role=user.rol.value,
            mode=data.mode,
        )

        return {
            "message": "Login exitoso",
            "access_token": access_token,
        }