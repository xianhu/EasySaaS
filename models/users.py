# _*_ coding: utf-8 _*_

"""
user model
"""

import hashlib

import sqlalchemy
from sqlalchemy import Index, func, orm
from werkzeug import security

try:
    from . import app_db
except ImportError:
    from models import app_db


class User(app_db.Model):
    __tablename__ = "users"
    __table_args__ = (
        Index("index_u_1", "name"),
        Index("index_u_2", "email"),
        Index("index_u_3", "phone"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.String(128), primary_key=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(512), nullable=False)

    # informations
    name = sqlalchemy.Column(sqlalchemy.String(128), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(128), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(128), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(128), nullable=True)

    # company
    company_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=True)
    company_avatar = sqlalchemy.Column(sqlalchemy.String(128), nullable=True)

    # address
    addr_state = sqlalchemy.Column(sqlalchemy.String(128), doc="state of address")
    addr_city = sqlalchemy.Column(sqlalchemy.String(128), doc="city of address")
    addr_detail = sqlalchemy.Column(sqlalchemy.String(128), doc="detail of address")

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="-1 0 1")
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), server_onupdate=func.now())

    def __init__(self, _id, pwd, name=None, avatar=None, email=None, phone=None, status=1):
        """
        init user
        """
        self.id = _id
        self.pwd = pwd
        self.name = name
        self.avatar = avatar
        self.email = email
        self.phone = phone
        self.status = status
        return

    def __repr__(self) -> str:
        """
        to string
        """
        col_list = [self.id, self.name, self.email, self.phone]
        return f"User <{' - '.join(map(str, col_list))}>"

    def to_json(self) -> dict:
        """
        to json
        """
        return {
            "id": self.id,
            "name": self.name,
            "avatar": self.avatar,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
        }


if __name__ == "__main__":
    from config import config_database_uri

    # create engine
    engine = sqlalchemy.create_engine(config_database_uri)

    # create all tables
    User.__table__.drop(engine, checkfirst=True)
    User.__table__.create(engine, checkfirst=True)

    # create session and add data
    with orm.sessionmaker(engine)() as session:
        _email = "aaaa@qq.com"
        _id = hashlib.md5(_email.encode()).hexdigest()
        _pwd = security.generate_password_hash(_email)
        _user = User(_id=_id, pwd=_pwd, email=_email)

        session.add(_user)
        session.commit()
        print(session.query(User).get(_id))
