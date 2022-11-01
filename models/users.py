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

    # print format
    def __repr__(self) -> str:
        return f"User <{' - '.join(map(str, [self.id, self.name, self.email, self.phone]))}>"


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
        _user = User(id=_id, pwd=_pwd, email=_email)

        session.add(_user)
        session.commit()
        print(session.query(User).get(_id))
