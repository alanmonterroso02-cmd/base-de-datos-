from fastapi import APIRouter, Request

from app.core.settings import BASE_DIR
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

pages_router = APIRouter()


@pages_router.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "pages/index.html")


@pages_router.get("/login")
def login_reciclador(request: Request):
    return templates.TemplateResponse(request, "pages/login/reciclador.html")


@pages_router.get("/login/colaborador")
def login_usuario(request: Request):
    return templates.TemplateResponse(request, "pages/login/usuario.html")


@pages_router.get("/reciclador/inicio")
def reciclador_inicio(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/inicio.html")


@pages_router.get("/reciclador/historial-puntos")
def reciclador_historial_puntos(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/historial_puntos.html")


@pages_router.get("/reciclador/premios")
def reciclador_premios(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/ver_premios.html")


@pages_router.get("/reciclador/mis-cupones")
def reciclador_mis_cupones(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/mis_cupones.html")


@pages_router.get("/usuario/inicio")
def usuario_inicio(request: Request):
    return templates.TemplateResponse(request, "pages/usuario/inicio.html")


@pages_router.get("/admin/dashboard")
def admin_dashboard(request: Request):
    return templates.TemplateResponse(request, "pages/admin/dashboard.html")


@pages_router.get("/admin/premios")
def admin_premios(request: Request):
    return templates.TemplateResponse(request, "pages/admin/premios.html")


@pages_router.get("/admin/usuarios")
def admin_usuarios(request: Request):
    return templates.TemplateResponse(request, "pages/admin/usuarios.html")


@pages_router.get("/admin/categorias")
def admin_categorias(request: Request):
    return templates.TemplateResponse(request, "pages/admin/categorias.html")


@pages_router.get("/admin/recicladores")
def admin_recicladores(request: Request):
    return templates.TemplateResponse(request, "pages/admin/recicladores.html")


@pages_router.get("/logout")
def logout(request: Request):
    response = templates.TemplateResponse(request, "pages/index.html")
    response.delete_cookie("token", path="/")
    response.delete_cookie("rol", path="/")
    return response
