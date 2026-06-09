from .db_config import engine
from sqlmodel import Session, SQLModel


def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    SQLModel.metadata.create_all(engine)
    _migrate_existing_tables()


def _migrate_existing_tables():
    from sqlalchemy import text, inspect
    with Session(engine) as session:
        inspector = inspect(engine)
        columns = [col["name"] for col in inspector.get_columns("categorias_reciclaje")]
        if "imagen" not in columns:
            session.exec(text("ALTER TABLE categorias_reciclaje ADD COLUMN imagen VARCHAR(255) NULL"))
            session.commit()
