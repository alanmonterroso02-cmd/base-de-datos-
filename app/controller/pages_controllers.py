from fastapi import APIRouter, Request
from config.config_app import templates

pages_routes = APIRouter()


@pages_routes.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "pages/index.html")


@pages_routes.get("/login")
def login_reciclador(request: Request):
    return templates.TemplateResponse(request, "pages/login.html")
