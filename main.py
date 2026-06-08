from fastapi import FastAPI
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

# base de datos
from database import create_tables
from database.db_config import engine
from app.models.categorias_reciclaje_model import CategoriaReciclajeModel

# controllers
from app.controller import reciclador_router, categoria_router, pages_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()

    with Session(engine) as session:
        existe = session.exec(select(CategoriaReciclajeModel)).first()

        if not existe:
            session.add_all(
                [
                    CategoriaReciclajeModel(
                        nombre="Plástico", puntos_por_gramo=0.10, activa=True
                    ),
                    CategoriaReciclajeModel(
                        nombre="Aluminio", puntos_por_gramo=0.20, activa=True
                    ),
                ]
            )

            session.commit()

    yield


app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pages_routes)
app.include_router(reciclador_router)
app.include_router(categoria_router)
