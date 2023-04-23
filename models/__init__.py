# _*_ coding: utf-8 _*_

"""
models module
"""

from typing import Any

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative
class BaseModel:
    __name__: str

    id: Any
    created_at: sqlalchemy.DateTime = sqlalchemy.Column(
        sqlalchemy.DateTime, default=func.now(), doc="Created At",
    )
    updated_at: sqlalchemy.DateTime = sqlalchemy.Column(
        sqlalchemy.DateTime, default=func.now(), onupdate=func.now(), doc="Updated At",
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
