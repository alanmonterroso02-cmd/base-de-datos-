from fastapi import APIRouter, Request
from config.config_app import templates

pages_routes = APIRouter()


@pages_routes.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "pages/index.html")


@pages_routes.get("/login")
def login_reciclador(request: Request):
    return templates.TemplateResponse(request, "pages/login/reciclador.html")


@pages_routes.get("/login/colaborador")
def login_usuario(request: Request):
    return templates.TemplateResponse(request, "pages/login/usuario.html")

@pages_routes.get("/reciclador/inicio")
def reciclador_inicio(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/inicio.html")


@pages_routes.get("/reciclador/historial-puntos")
def reciclador_historial_puntos(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/historial_puntos.html")


@pages_routes.get("/reciclador/premios")
def reciclador_premios(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/ver_premios.html")

@pages_routes.get("/reciclador/mis-cupones")
def reciclador_mis_cupones(request: Request):
    return templates.TemplateResponse(request, "pages/reciclador/mis_cupones.html")
