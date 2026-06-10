from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

from app.core.database import create_tables, engine
from app.models.categoria_reciclaje import CategoriaReciclaje
from app.models.usuario import Usuario, RolEnum
from app.utils.password import hash_password
from app.routers import (
    auth_router,
    recicladores_router,
    categorias_router,
    usuarios_router,
    premios_router,
    cupones_router,
)
from app.views import (
    public_views_router,
    auth_views_router,
    admin_views_router,
    reciclador_views_router,
    colaborador_views_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()

    with Session(engine) as session:
        existe = session.exec(select(CategoriaReciclaje)).first()

        if not existe:
            session.add_all(
                [
                    CategoriaReciclaje(nombre="Plástico", puntos_por_gramo=0.10),
                    CategoriaReciclaje(nombre="Aluminio", puntos_por_gramo=0.20),
                ]
            )
            session.commit()

        existe_usuario = session.exec(select(Usuario)).first()

        if not existe_usuario:
            admin = Usuario(
                nombre_completo="Admin Principal",
                correo="admin@ecodesarrolladores.com",
                contrasena=hash_password("admin123"),
                rol=RolEnum.Admin,
            )
            colaborador = Usuario(
                nombre_completo="Colaborador Principal",
                correo="colaborador@ecodesarrolladores.com",
                contrasena=hash_password("colab123"),
                rol=RolEnum.Colaborador,
            )
            session.add_all([admin, colaborador])
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

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
app.include_router(auth_router)
app.include_router(recicladores_router)
app.include_router(categorias_router)
app.include_router(usuarios_router)
app.include_router(premios_router)
app.include_router(cupones_router)
app.include_router(public_views_router)
app.include_router(auth_views_router)
app.include_router(admin_views_router)
app.include_router(reciclador_views_router)
app.include_router(colaborador_views_router)
