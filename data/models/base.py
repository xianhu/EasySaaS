# _*_ coding: utf-8 _*_

"""
base model
"""

from typing import Any, Dict

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.ext import declarative

# define base model
Model = declarative.declarative_base()
exclude_fields = ("created_at", "updated_at")


class AbstractModel(Model):
    __abstract__ = True

    @declarative.declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def get(self, field: str) -> Any:
        return getattr(self, field)

    def dict(self, exclude=exclude_fields) -> Dict[str, Any]:
        columns = [c for c in self.__table__.columns if c.name not in exclude]
        return {c.name: getattr(self, c.name) for c in columns}

    # information -- id, status, created_at, updated_at
    id = sqlalchemy.Column(sqlalchemy.String(128), primary_key=True)
    status = sqlalchemy.Column(sqlalchemy.SmallInteger, default=1, doc="Status: 1/0")
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=func.now(), doc="Created At")
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=func.now(), onupdate=func.now(), doc="Updated At")
