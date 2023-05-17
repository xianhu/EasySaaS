# _*_ coding: utf-8 _*_

"""
base crud
"""

from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..models.base import Model

# define generic type
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model
        return

    def get(self, session: Session, _id: int) -> Optional[ModelType]:
        obj_model = session.query(self.model).get(_id)
        return obj_model

    def get_multi(self, session: Session, offset: int = 0, limit: int = 100) -> List[ModelType]:
        obj_model_list = session.query(self.model).offset(offset).limit(limit).all()
        return obj_model_list

    def delete(self, session: Session, _id: int) -> Optional[ModelType]:
        obj_model = session.query(self.model).get(_id)
        session.delete(obj_model)
        session.commit()
        # session.refresh(obj_model)
        return obj_model

    def create(self, session: Session, obj_schema: CreateSchemaType) -> ModelType:
        obj_schema = obj_schema.dict(exclude_unset=True)  # include default value
        obj_model = self.model(**obj_schema)
        session.add(obj_model)
        session.commit()
        session.refresh(obj_model)
        return obj_model

    def update(self, session: Session, obj_model: ModelType, obj_schema: UpdateSchemaType) -> ModelType:
        obj_schema = obj_schema.dict(exclude_unset=True, exclude_defaults=True)
        [setattr(obj_model, field, obj_schema[field]) for field in obj_schema]
        session.merge(obj_model)
        session.commit()
        session.refresh(obj_model)
        return obj_model
