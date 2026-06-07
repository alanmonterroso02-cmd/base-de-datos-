from .db_config import engine
from sqlmodel import Session, SQLModel


def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    SQLModel.metadata.create_all(engine)
