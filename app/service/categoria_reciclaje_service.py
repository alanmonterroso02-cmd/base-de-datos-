from sqlmodel import Session, select
from fastapi import HTTPException, status
from uuid import UUID

from app.models.categorias_reciclaje_model import CategoriaReciclajeModel
from app.schema.categoria_reciclaje import CategoriaReciclajeOut, CategoriaReciclajeCreate, CategoriaReciclajeUpdate


class CategoriaReciclajeService:
    def __init__(self, session: Session):
        self.session = session

    def obtener_categoria(self, categoria_id: UUID) -> CategoriaReciclajeModel | None:
        return self.session.get(CategoriaReciclajeModel, categoria_id)

    def crear_categoria(self, data: CategoriaReciclajeCreate) -> CategoriaReciclajeModel:
        nueva = CategoriaReciclajeModel.model_validate(data)
        self.session.add(nueva)
        self.session.commit()
        self.session.refresh(nueva)
        return nueva

    def actualizar_categoria(self, categoria_id: UUID, data: CategoriaReciclajeUpdate) -> CategoriaReciclajeModel:
        categoria = self.obtener_categoria(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(categoria, key, value)

        self.session.add(categoria)
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def obtener_para_formulario(self):
        statement = (
            select(CategoriaReciclajeModel)
            .where(CategoriaReciclajeModel.activa == True)
            .order_by(CategoriaReciclajeModel.nombre)
        )

        rows = self.session.exec(statement).all()

        return [CategoriaReciclajeOut.model_validate(row) for row in rows]
