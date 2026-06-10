from fastapi import APIRouter, Request

from app.core.settings import BASE_DIR
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

router = APIRouter()


@router.get("/admin/dashboard")
def admin_dashboard(request: Request):
    return templates.TemplateResponse(request, "pages/admin/dashboard.html")


@router.get("/admin/premios")
def admin_premios(request: Request):
    return templates.TemplateResponse(request, "pages/admin/premios.html")


@router.get("/admin/usuarios")
def admin_usuarios(request: Request):
    return templates.TemplateResponse(request, "pages/admin/usuarios.html")


@router.get("/admin/categorias")
def admin_categorias(request: Request):
    return templates.TemplateResponse(request, "pages/admin/categorias.html")


@router.get("/admin/recicladores")
def admin_recicladores(request: Request):
    return templates.TemplateResponse(request, "pages/admin/recicladores.html")
