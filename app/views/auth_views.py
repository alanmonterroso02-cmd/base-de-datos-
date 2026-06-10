from fastapi import APIRouter, Request

from app.core.settings import BASE_DIR
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

router = APIRouter()


@router.get("/login")
def login_reciclador(request: Request):
    return templates.TemplateResponse(request, "pages/login/reciclador.html")


@router.get("/login/colaborador")
def login_colaborador(request: Request):
    return templates.TemplateResponse(request, "pages/login/usuario.html")


@router.get("/logout")
def logout(request: Request):
    response = templates.TemplateResponse(request, "pages/index.html")
    response.delete_cookie("token", path="/")
    response.delete_cookie("rol", path="/")
    return response
