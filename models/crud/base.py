# _*_ coding: utf-8 _*_

"""
base crud
"""

from typing import Generic, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..base import Model

# define generic type
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model
        return

    def get(self, db: Session, _id: Union[int, str]) -> Optional[ModelType]:
        obj_db = db.query(self.model).get(_id)
        return obj_db

    def delete(self, db: Session, _id: Union[int, str]) -> ModelType:
        obj_db = db.query(self.model).get(_id)
        obj_db.status = 0
        db.commit()
        db.refresh(obj_db)
        return obj_db

    def recover(self, db: Session, _id: Union[int, str]) -> ModelType:
        obj_db = db.query(self.model).get(_id)
        obj_db.status = 1
        db.commit()
        db.refresh(obj_db)
        return obj_db

    def create(self, db: Session, obj_schema: CreateSchemaType) -> ModelType:
        obj_schema = obj_schema.dict(exclude_unset=True, exclude_none=True)
        obj_db = self.model(**obj_schema)
        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)
        return obj_db

    def update(self, db: Session, obj_db: ModelType) -> ModelType:
        db.merge(obj_db)
        db.commit()
        db.refresh(obj_db)
        return obj_db

    def update_by_schema(self, db: Session, obj_db: ModelType, obj_schema: UpdateSchemaType) -> ModelType:
        obj_schema = obj_schema.dict(exclude_unset=True, exclude_none=True)
        [setattr(obj_db, field, obj_schema[field]) for field in obj_schema]
        return self.update(db, obj_db=obj_db)
