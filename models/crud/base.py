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
    """
    CRUD object with default methods to Create, Read, Update, Delete.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model
        return

    def get(self, db: Session, _id: Union[int, str]) -> Optional[ModelType]:
        obj = db.query(self.model).get(_id)
        return obj

    def delete(self, db: Session, _id: Union[int, str]) -> ModelType:
        obj = db.query(self.model).get(_id)
        obj.status = 0
        db.commit()
        return obj

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in = obj_in.dict(exclude_none=True)
        obj_db = self.model(**obj_in)
        db.add(obj_db)
        db.commit()
        return obj_db

    def update(self, db: Session, obj_db: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_in = obj_in.dict(exclude_none=True)
        [setattr(obj_db, field, obj_in[field]) for field in obj_in]
        db.merge(obj_db)
        db.commit()
        return obj_db
