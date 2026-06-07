from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from config.config_app import templates
from database import create_tables
from database.db_config import engine

from app.models.categorias_reciclaje_model import CategoriaReciclajeModel
from app.controller.resicladores_controller import reciclador_router
from app.controller.categoria_reciclaje_controller import categoria_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()

    with Session(engine) as session:
        existe = session.exec(
            select(CategoriaReciclajeModel)
        ).first()

        if not existe:
            session.add_all([
                CategoriaReciclajeModel(
                    nombre="Plástico",
                    puntos_por_gramo=0.10,
                    activa=True
                ),
                CategoriaReciclajeModel(
                    nombre="Aluminio",
                    puntos_por_gramo=0.20,
                    activa=True
                )
            ])

            session.commit()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/index.html"
    )


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(reciclador_router)
app.include_router(categoria_router)