from fastapi import APIRouter, Request, Form, Depends, BackgroundTasks

from ...service.usuarios_autenticacion_service import UsuariosAutenticacionService
from ...schemas.login_user import LoginRequestSchema
from ...schemas.create_user import CreateUserRequestSchema
from ...util.mail_service import MailService
from config.config_app import templates

usuarios_autenticacion = APIRouter()


@usuarios_autenticacion.get("/create")
async def create_web(request: Request):
    return templates.TemplateResponse(request, "pages/authentication/create.html")


@usuarios_autenticacion.get("/login")
async def login_web(request: Request):
    return templates.TemplateResponse(request, "pages/authentication/login.html")


@usuarios_autenticacion.post("/login")
async def login_api(
    data: LoginRequestSchema = Form(),
    service: UsuariosAutenticacionService = Depends(),
):
    return await service.login(data)


@usuarios_autenticacion.post("/create")
async def create_api(
    background_tasks: BackgroundTasks,
    data: CreateUserRequestSchema = Form(),
    service: UsuariosAutenticacionService = Depends(),
):
    result = await service.create(data)

    background_tasks.add_task(
        MailService.send_mail,
        result["correo"],             
        "Credenciales de acceso",
        "user_created.html",
        result["context"],
    )

    return {"message": "Revisa tu correo para ver tus credenciales."}