from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from app.util.jwt_manager import validate_token
from app.models.usuario_model import RolEnum

security = HTTPBearer(auto_error=False)


def _get_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
    try:
        return validate_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def get_current_reciclador(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
):
    payload = _get_token_payload(credentials)
    if "nit" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return payload


def get_current_usuario(payload: dict = Depends(_get_token_payload)) -> dict:
    """Valida que el token pertenezca a un usuario (tiene 'rol')."""
    if "rol" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return payload


def require_rol(*roles: RolEnum):
    """Factoría: devuelve una dependencia que exige uno de los roles dados."""
    def dependency(usuario: dict = Depends(get_current_usuario)) -> dict:
        if usuario["rol"] not in [r.value for r in roles]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
        return usuario
    return dependency


# Dependencias listas para usar
require_colaborador = require_rol(RolEnum.Colaborador, RolEnum.Admin)  # Admin también puede
require_admin       = require_rol(RolEnum.Admin)