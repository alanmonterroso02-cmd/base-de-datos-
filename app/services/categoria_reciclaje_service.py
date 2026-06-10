from fastapi import HTTPException, status
from uuid import UUID

from app.repositories.categorias_repository import CategoriaReciclajeRepository
from app.models.categoria_reciclaje import CategoriaReciclaje
from app.schemas.categoria_reciclaje import (
    CategoriaReciclajeOut,
    CategoriaReciclajeCreate,
    CategoriaReciclajeUpdate,
)


class CategoriaReciclajeService:
    def __init__(self, repository: CategoriaReciclajeRepository):
        self.repo = repository

    def obtener_categoria(self, categoria_id: UUID) -> CategoriaReciclaje | None:
        return self.repo.find_by_id(categoria_id)

    def crear_categoria(self, data: CategoriaReciclajeCreate) -> CategoriaReciclaje:
        nueva = CategoriaReciclaje.model_validate(data)
        return self.repo.add(nueva)

    def actualizar_categoria(
        self, categoria_id: UUID, data: CategoriaReciclajeUpdate
    ) -> CategoriaReciclaje:
        categoria = self.obtener_categoria(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(categoria, key, value)

        return self.repo.update(categoria)

    def listar_categorias(self):
        rows = self.repo.get_all()
        return [CategoriaReciclajeOut.model_validate(r) for r in rows]
