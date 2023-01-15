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

    # get function
    def get(self, column):
        return getattr(self, column)

    # to dict function
    def to_dict(self) -> dict:
        columns = self.__table__.columns
        return {c.name: getattr(self, c.name) for c in columns}

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="-1 0 1")
    datetime_created = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_updated = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), server_onupdate=func.now())
