from sqlmodel import Session
from config.config_app import templates
from fastapi import APIRouter, Depends, Form, HTTPException, Request

from database import get_session
from app.util.auth import get_current_reciclador
from app.service.recicladores_service import RecicladorService
from ..schema.material_resiclado import MaterialRecicladoSchema

reciclador_router = APIRouter(prefix="/reciclador", tags=["Reciclador"])


@reciclador_router.post("/login")
def login_reciclador(nit: int = Form(...), session: Session = Depends(get_session)):
    service = RecicladorService(session)

    response = service.login(nit)

    if not response:
        raise HTTPException(status_code=404, detail="nit no encontrado")

    return response


@reciclador_router.post("/puntos/agregar")
def agregar_puntos(
    data: MaterialRecicladoSchema,
    reciclador=Depends(get_current_reciclador),
    session: Session = Depends(get_session),
):
    service = RecicladorService(session)

    return service.agregar_puntos(reciclador["nit"], data)
