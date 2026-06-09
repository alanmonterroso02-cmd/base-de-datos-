from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.models.usuario_model import UsuariosModel
from app.util.password import hash_password, verify_password
from app.util.jwt_manager import create_token

class UsuariosService:
    def __init__(self, session: Session):
        self.session = session

    def registrar_usuario(self, usuario_data):
        usuario_existente = self.obtener_usuario_por_correo(usuario_data.correo)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado"
            )

        # Hashear la contraseña
        password_hashed = hash_password(usuario_data.contrasena)

        # Crear nuevo usuario
        nuevo_usuario = UsuariosModel(
            nombre_completo=usuario_data.nombre_completo,
            correo=usuario_data.correo,
            contrasena=password_hashed,
            rol=usuario_data.rol
        )

        self.session.add(nuevo_usuario)
        self.session.commit()
        self.session.refresh(nuevo_usuario)

        return {
            "id": nuevo_usuario.id,
            "nombre_completo": nuevo_usuario.nombre_completo,
            "correo": nuevo_usuario.correo,
            "rol": nuevo_usuario.rol
        }

    def autenticar_usuario(self, correo: str, contrasena: str):
        usuario = self.obtener_usuario_por_correo(correo)

        if not usuario or not verify_password(contrasena, usuario.contrasena):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos"
            )

        # Crear token JWT
        token = create_token({
            "id": str(usuario.id),
            "correo": usuario.correo,
            "rol": usuario.rol.value
        })

        return {
            "token": token,
            "tipo": "bearer",
            "usuario": {
                "nombre": usuario.nombre_completo,
                "rol": usuario.rol.value
            }
        }

    def obtener_usuario_por_correo(self, correo: str) -> UsuariosModel | None:
        return self.session.exec(
            select(UsuariosModel).where(UsuariosModel.correo == correo)
        ).first()
