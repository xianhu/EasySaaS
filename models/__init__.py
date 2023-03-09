# _*_ coding: utf-8 _*_

"""
models module
"""

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class BaseModel(app_db.Model):
    __abstract__ = True
    __ignore__ = ["datetime_created", "datetime_updated"]

    # get function
    def get(self, column):
        return getattr(self, column)

    # to dict function
    def to_dict(self) -> dict:
        columns = [c for c in self.__table__.columns if c.name not in self.__ignore__]
        return {c.name: getattr(self, c.name) for c in columns}

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="1/0")
    datetime_created = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_updated = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), server_onupdate=func.now())
