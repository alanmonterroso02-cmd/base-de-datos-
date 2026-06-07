from sqlmodel import Session, select

from app.models.categorias_reciclaje_model import CategoriaReciclajeModel


class CategoriaReciclajeService:
    def __init__(self, session: Session):
        self.session = session

    def obtener_para_formulario(self):

        statement = (
            select(CategoriaReciclajeModel)
            .where(CategoriaReciclajeModel.activa == True)
            .order_by(CategoriaReciclajeModel.nombre)
        )

        return self.session.exec(statement).all()
