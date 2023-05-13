# _*_ coding: utf-8 _*_

"""
base crud
"""

from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..models import Model

# define generic type
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
UpdatePriSchemaType = TypeVar("UpdatePriSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, UpdatePriSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model
        return

    def get(self, session: Session, _id: int) -> Optional[ModelType]:
        obj_db = session.query(self.model).get(_id)
        return obj_db

    def get_multi(self, session: Session, offset: int = 0, limit: int = 100) -> List[ModelType]:
        obj_db_list = session.query(self.model).offset(offset).limit(limit).all()
        return obj_db_list

    def delete(self, session: Session, _id: int) -> Optional[ModelType]:
        obj_db = session.query(self.model).get(_id)
        session.delete(obj_db)
        session.commit()
        # session.refresh(obj_db)
        return obj_db

    def create(self, session: Session, obj_schema: CreateSchemaType) -> ModelType:
        obj_schema = obj_schema.dict(exclude_unset=True, exclude_defaults=True)
        obj_db = self.model(**obj_schema)
        session.add(obj_db)
        session.commit()
        session.refresh(obj_db)
        return obj_db

    def update(self, session: Session, obj_db: ModelType, obj_schema: UpdateSchemaType) -> ModelType:
        obj_schema = obj_schema.dict(exclude_unset=True, exclude_defaults=True)
        [setattr(obj_db, field, obj_schema[field]) for field in obj_schema]
        session.merge(obj_db)
        session.commit()
        session.refresh(obj_db)
        return obj_db

    def update_pri(self, session: Session, obj_db: ModelType, obj_schema: UpdatePriSchemaType) -> ModelType:
        obj_schema = obj_schema.dict(exclude_unset=True, exclude_defaults=True)
        [setattr(obj_db, field, obj_schema[field]) for field in obj_schema]
        session.merge(obj_db)
        session.commit()
        session.refresh(obj_db)
        return obj_db
