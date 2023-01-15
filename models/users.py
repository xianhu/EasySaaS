# _*_ coding: utf-8 _*_

"""
user model
"""

import hashlib
import logging

import sqlalchemy
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
    avatar = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)

    # authentication
    auth_github = sqlalchemy.Column(sqlalchemy.String(512), doc="token of github")
    auth_google = sqlalchemy.Column(sqlalchemy.String(512), doc="token of google")


class Team(BaseModel):
    __tablename__ = "teams"
    __table_args__ = (
        sqlalchemy.Index("index_t_1", "name"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)

    # informations
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)

    # informations
    ts_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ts_expired = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)


class TeamUser(BaseModel):
    __tablename__ = "team_users"
    __table_args__ = (
        sqlalchemy.Index("index_tu_1", "user_id"),
        sqlalchemy.Index("index_tu_2", "team_id"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # relations
    user_id = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    team_id = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    # informations
    role = sqlalchemy.Column(sqlalchemy.String(255), default="admin", doc="admin/member")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, doc="json of role")


if __name__ == "__main__":
    from sqlalchemy import orm
    from config import config_database_uri

    # create engine
    engine = sqlalchemy.create_engine(config_database_uri)

    # create all tables
    User.__table__.drop(engine, checkfirst=True)
    User.__table__.create(engine, checkfirst=True)
    logging.warning("create table success: %s", User.__tablename__)

    Team.__table__.drop(engine, checkfirst=True)
    Team.__table__.create(engine, checkfirst=True)
    logging.warning("create table success: %s", Team.__tablename__)

    TeamUser.__table__.drop(engine, checkfirst=True)
    TeamUser.__table__.create(engine, checkfirst=True)
    logging.warning("create table success: %s", TeamUser.__tablename__)

    # create session and add data
    _email = "admin@easysaas.com"
    with orm.sessionmaker(engine)() as session:
        _id = hashlib.md5(_email.encode()).hexdigest()
        _pwd = security.generate_password_hash(_email)
        _user = User(id=_id, pwd=_pwd, email=_email, name="admin")

        try:
            session.add(_user)
            session.commit()
            logging.warning("add user success: %s", _user.to_dict())
        except Exception as excep:
            logging.error("add user failed: %s", excep)
            session.rollback()

    # create session and add data
    _name = "demo team"
    with orm.sessionmaker(engine)() as session:
        _user = session.query(User).filter(User.email == _email).first()

        _id = hashlib.md5(_name.encode()).hexdigest()
        _team = Team(id=_id, name=_name, ts_start=None, ts_expired=None)
        _team_user = TeamUser(user_id=_user.get("id"), team_id=_team.get("id"), role="admin")

        try:
            session.add(_team)
            session.add(_team_user)
            session.commit()
            logging.warning("add team success: %s", _team.to_dict())
        except Exception as excep:
            logging.error("add team failed: %s", excep)
            session.rollback()
