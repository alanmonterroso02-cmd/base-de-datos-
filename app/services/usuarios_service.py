from fastapi import HTTPException, status

from app.repositories.usuarios_repository import UsuarioRepository
from app.utils.password import hash_password, verify_password
from app.utils.jwt_manager import create_token


class UsuariosService:
    def __init__(self, repository: UsuarioRepository):
        self.repo = repository

    def registrar_usuario(self, usuario_data):
        existente = self.repo.find_by_correo(usuario_data.correo)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado",
            )

        from app.models.usuario import Usuario

        nuevo = Usuario(
            nombre_completo=usuario_data.nombre_completo,
            correo=usuario_data.correo,
            contrasena=hash_password(usuario_data.contrasena),
            rol=usuario_data.rol,
        )
        self.repo.add(nuevo)

        return {
            "id": nuevo.id,
            "nombre_completo": nuevo.nombre_completo,
            "correo": nuevo.correo,
            "rol": nuevo.rol,
        }

    def autenticar_usuario(self, correo: str, contrasena: str):
        usuario = self.repo.find_by_correo(correo)
        if not usuario or not verify_password(contrasena, usuario.contrasena):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos",
            )

        token = create_token(
            {
                "id": str(usuario.id),
                "correo": usuario.correo,
                "rol": usuario.rol.value,
            }
        )

        return {
            "token": token,
            "tipo": "bearer",
            "usuario": {
                "nombre": usuario.nombre_completo,
                "rol": usuario.rol.value,
            },
        }

    def obtener_usuario_por_id(self, usuario_id: str):
        return self.repo.find_by_id(usuario_id)

    def eliminar_usuario(self, usuario_id: str):
        usuario = self.repo.find_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya está desactivado",
            )
        usuario.activo = False
        self.repo.update(usuario)
        return {"mensaje": "Usuario desactivado correctamente"}

    def reactivar_usuario(self, usuario_id: str):
        usuario = self.repo.find_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        if usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya está activo",
            )
        usuario.activo = True
        self.repo.update(usuario)
        return {"mensaje": "Usuario reactivado correctamente"}

    def listar_usuarios(self):
        usuarios = self.repo.get_all()
        return [
            {
                "id": str(u.id),
                "nombre_completo": u.nombre_completo,
                "correo": u.correo,
                "rol": u.rol.value,
                "activo": u.activo,
            }
            for u in usuarios
        ]
