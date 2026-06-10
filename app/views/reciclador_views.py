from fastapi import APIRouter, Request

from app.core.settings import BASE_DIR
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

router = APIRouter()


@router.get("/reciclador/inicio")
def reciclador_inicio(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/inicio.html")


@router.get("/reciclador/historial-puntos")
def reciclador_historial_puntos(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/historial_puntos.html")


@router.get("/reciclador/premios")
def reciclador_premios(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/ver_premios.html")


@router.get("/reciclador/mis-cupones")
def reciclador_mis_cupones(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/mis_cupones.html")
