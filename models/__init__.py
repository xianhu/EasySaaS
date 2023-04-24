# _*_ coding: utf-8 _*_

"""
models module
"""

from typing import Generator

import sqlalchemy.orm
from sqlalchemy import func
from sqlalchemy.ext import declarative

from core.settings import settings

# create engine and session_maker
engine = sqlalchemy.create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False, autoflush=True)


def get_session() -> Generator:
    """
    get session, {for _ in get_session(): pass}
    :return: generator object
    """
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


# define base model
Model = declarative.declarative_base()


class BaseModel(Model):
    __abstract__ = True
    __ignore__ = ["pwd", "created_at", "updated_at"]

    @declarative.declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    # get function
    def get(self, column) -> object:
        return getattr(self, column)

    # to dict function
    def to_dict(self) -> dict:
        columns = [c for c in self.__table__.columns if c.name not in self.__ignore__]
        return {c.name: getattr(self, c.name) for c in columns}

    status = sqlalchemy.Column(sqlalchemy.SmallInteger, default=1, doc="Status: 1/0")
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=func.now(), doc="Created At")
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=func.now(), onupdate=func.now(), doc="Updated At")
