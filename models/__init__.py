# _*_ coding: utf-8 _*_

"""
models module
"""

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative
class BaseModel:
    __name__: str

    status: sqlalchemy.SmallInteger = sqlalchemy.Column(
        sqlalchemy.SmallInteger, default=1, doc="Status of 1/0",
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


class UserBase(BaseModel):
    # basic
    id = sqlalchemy.Column(sqlalchemy.String(255), index=True, primary_key=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(512), index=False, nullable=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(255), index=True, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(255), index=False, nullable=True)
