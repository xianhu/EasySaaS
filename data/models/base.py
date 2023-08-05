# _*_ coding: utf-8 _*_

"""
base model
"""

from datetime import datetime
from typing import Any, Dict

import sqlalchemy
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.ext import declarative

__all__ = ["sqlalchemy", "ForeignKey", "UniqueConstraint", "AbstractModel"]

# define base model
Model = declarative.declarative_base()

# define exclude fields
_g_exclude_fields = ("status", "created_at", "updated_at")


class AbstractModel(Model):
    __abstract__ = True

    @classmethod
    @declarative.declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def get(self, field: str) -> Any:
        return getattr(self, field)

    def dict(self, exclude_fields: tuple | list = _g_exclude_fields) -> Dict[str, Any]:
        columns = [c for c in self.__table__.columns if c.name not in exclude_fields]
        return {c.name: getattr(self, c.name) for c in columns}

    # information -- id, status, created_at, updated_at
    id = sqlalchemy.Column(sqlalchemy.String(128), primary_key=True)
    status = sqlalchemy.Column(sqlalchemy.SmallInteger, default=1, doc="Status: 1/0")
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, doc="Created At")
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, doc="Updated At")
