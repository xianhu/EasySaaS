# _*_ coding: utf-8 _*_

"""
models module
"""

from flask_sqlalchemy import SQLAlchemy

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class BaseModel(app_db.Model):
    """
    base model
    """
    __abstract__ = True

    # get function
    def get(self, column):
        return getattr(self, column)

    # to dict function
    def to_dict(self) -> dict:
        columns = self.__table__.columns
        return {c.name: getattr(self, c.name) for c in columns}
