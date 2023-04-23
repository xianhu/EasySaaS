# _*_ coding: utf-8 _*_

"""
models in flask
"""

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class BaseModel(app_db.Model):
    __abstract__ = True
    __ignore__ = ["created_at", "updated_at"]

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    # get function
    def get(self, column):
        return getattr(self, column)

    # to dict function
    def to_dict(self) -> dict:
        columns = [c for c in self.__table__.columns if c.name not in self.__ignore__]
        return {c.name: getattr(self, c.name) for c in columns}

    status = sqlalchemy.Column(sqlalchemy.SmallInteger, default=1, doc="Status: 1/0")
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=func.now(), doc="Created At")
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=func.now(), onupdate=func.now(), doc="Updated At")
