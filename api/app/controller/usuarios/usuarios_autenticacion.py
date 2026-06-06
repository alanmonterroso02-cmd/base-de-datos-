from sqlmodel import Session
from fastapi import APIRouter, Request, Form, Depends, BackgroundTasks

# db
from database import get_session

# util
from config.config_app import templates
from ...util.mail_service import MailService

# schemas
from ...schemas.login_user import LoginRequestSchema
from ...schemas.create_user import CreateUserRequestSchema

# servise
from ...service.usuarios_autenticacion_service import UsuariosAutenticacionService


usuarios_autenticacion_route = APIRouter()


@usuarios_autenticacion_route.get("/create")
async def create_web(request: Request):
    return templates.TemplateResponse(request, "pages/authentication/create.html")


@usuarios_autenticacion_route.get("/login")
async def login_web(request: Request):
    return templates.TemplateResponse(request, "pages/authentication/login.html")


@usuarios_autenticacion_route.post("/login")
def login_api(
    data: LoginRequestSchema = Form(),
    session: Session = Depends(get_session),
):
    service = UsuariosAutenticacionService(session)
    return service.login(data)


@usuarios_autenticacion_route.post("/create")
def create_api(
    background_tasks: BackgroundTasks,
    data: CreateUserRequestSchema = Form(),
    session: Session = Depends(get_session),
):
    service = UsuariosAutenticacionService(session)

    result = service.create(data)

    background_tasks.add_task(
        MailService.send_mail,
        result["correo"],
        "Credenciales de acceso",
        "user_created.html",
        result["context"],
    )

    return {"message": "Revisa tu correo para ver tus credenciales."}
