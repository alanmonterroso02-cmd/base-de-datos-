from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

# base de datos
from database import create_tables
from database.db_config import engine
from app.models.categorias_reciclaje_model import CategoriaReciclajeModel


# controllers
from app.controller import reciclador_router, categoria_router, pages_routes, usuarios_router, premios_router


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pages_routes)
app.include_router(reciclador_router)
app.include_router(categoria_router)
app.include_router(usuarios_router)
app.include_router(premios_router)
