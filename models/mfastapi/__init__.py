# _*_ coding: utf-8 _*_

"""
models in fastapi
"""

import sqlalchemy.orm
from sqlalchemy import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from core.settings import settings

engine = sqlalchemy.create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False)


@as_declarative()
class BaseModel:
    __name__: str

    status: sqlalchemy.SmallInteger = sqlalchemy.Column(
        sqlalchemy.SmallInteger, default=1, doc="Status: 1/0",
    )
    created_at: sqlalchemy.DateTime = sqlalchemy.Column(
        sqlalchemy.DateTime, default=func.now(), doc="Created At",
    )
    updated_at: sqlalchemy.DateTime = sqlalchemy.Column(
        sqlalchemy.DateTime, default=func.now(), onupdate=func.now(), doc="Updated At",
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
