from fastapi import APIRouter, Request

from app.core.settings import BASE_DIR
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

router = APIRouter()


@router.get("/usuario/inicio")
def usuario_inicio(request: Request):
    return templates.TemplateResponse(request, "pages/usuario/inicio.html")


@router.get("/usuario/recicladores")
def usuario_recicladores(request: Request):
    return templates.TemplateResponse(request, "pages/usuario/recicladores.html")


@router.get("/usuario/canje")
def usuario_canje(request: Request):
    return templates.TemplateResponse(request, "pages/usuario/canje.html")
