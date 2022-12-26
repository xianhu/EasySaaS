# _*_ coding: utf-8 _*_

"""
user model
"""

import hashlib
import logging

import sqlalchemy
from sqlalchemy import func
from werkzeug import security

from models import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = (
        sqlalchemy.Index("index_u_1", "name"),
        sqlalchemy.Index("index_u_2", "email"),
        sqlalchemy.Index("index_u_3", "phone"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(512), nullable=False)

    # informations
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)

    # informations
    ts_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ts_expired = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    # company
    company_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    company_avatar = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)

    # address
    addr_state = sqlalchemy.Column(sqlalchemy.String(255), doc="state of address")
    addr_city = sqlalchemy.Column(sqlalchemy.String(255), doc="city of address")
    addr_detail = sqlalchemy.Column(sqlalchemy.String(1024), doc="detail of address")

    # authentication
    auth_github = sqlalchemy.Column(sqlalchemy.String(255), doc="token of github")
    auth_google = sqlalchemy.Column(sqlalchemy.String(255), doc="token of google")

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="-1 0 1")
    datetime_created = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_updated = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), server_onupdate=func.now())


if __name__ == "__main__":
    from sqlalchemy import orm
    from config import config_database_uri

    # create engine
    engine = sqlalchemy.create_engine(config_database_uri)

    # create all tables
    User.__table__.drop(engine, checkfirst=True)
    User.__table__.create(engine, checkfirst=True)
    logging.warning("create table success: %s", User.__tablename__)

    # create session and add data
    with orm.sessionmaker(engine)() as session:
        _email = "admin@easysaas.com"
        _id = hashlib.md5(_email.encode()).hexdigest()
        _pwd = security.generate_password_hash(_email)
        _user = User(id=_id, pwd=_pwd, email=_email)

        session.add(_user)
        session.commit()
        logging.warning("create user success: %s", _user.get("email"))

        _user = session.query(User).filter(
            User.email == _email
        ).first()
        _user_dict = _user.to_dict()
        logging.warning("get user success: %s", _user_dict)
