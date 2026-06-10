from typing import Generic, TypeVar, Type, Optional
from uuid import UUID
from sqlmodel import SQLModel, Session, select

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model

    def get(self, id: UUID | int) -> Optional[ModelType]:
        return self.session.get(self.model, id)

    def get_all(self) -> list[ModelType]:
        return self.session.exec(select(self.model)).all()

    def add(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def update(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def delete(self, instance: ModelType) -> None:
        self.session.delete(instance)
        self.session.commit()

    def find_by(self, **kwargs) -> Optional[ModelType]:
        stmt = select(self.model)
        for key, value in kwargs.items():
            column = getattr(self.model, key, None)
            if column is not None:
                stmt = stmt.where(column == value)
        return self.session.exec(stmt).first()
