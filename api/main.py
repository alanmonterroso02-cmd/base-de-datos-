from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from config.config_app import templates
from database import create_tables
from app.controller.usuarios.usuarios_autenticacion import usuarios_autenticacion


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "pages/index.html")


app.include_router(usuarios_autenticacion)