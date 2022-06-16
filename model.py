# _*_ coding: utf-8 _*_

"""
Model Defination
"""

import datetime
import hashlib

import sqlalchemy
from sqlalchemy import ForeignKey, func, orm
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security

from config import config_database_uri

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class BaseModel:
    """
    base model
    """
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="0 or 1")
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now())


class User(app_db.Model, BaseModel):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(500), nullable=False)
    admin = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="0 or 1")

    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)

    filename = sqlalchemy.Column(sqlalchemy.String(500), doc="file name")
    session = sqlalchemy.Column(sqlalchemy.String(500), doc="session value")
    tempcol = sqlalchemy.Column(sqlalchemy.String(500), doc="temporary column")

    # foreign key and relationship
    organ_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("organizations.id"))
    organization = orm.relationship("Organization", backref=orm.backref("users"))

    # print format
    def __repr__(self) -> str:
        col_list = [self.id, self.name, self.admin, self.email, self.phone, self.organ_id, self.status]
        return f"User <{' - '.join(map(str, col_list))}>"


class Organization(app_db.Model, BaseModel):
    __tablename__ = "organizations"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)

    avatar = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)

    plan_title = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    plan_expire = sqlalchemy.Column(sqlalchemy.DateTime, doc="expire datetime")

    # print format
    def __repr__(self) -> str:
        col_list = [self.id, self.name, self.plan_title, self.plan_expire, self.status]
        return f"Organizations <{' - '.join(map(str, col_list))}>"


def init_db():
    """
    initial database
    """
    # create engine, SQLite doesn't check the forgien key
    engine = sqlalchemy.create_engine(config_database_uri)

    # drop or create all tables
    app_db.Model.metadata.drop_all(engine)
    app_db.Model.metadata.create_all(engine)


def add_user(email="aaaa@qq.com", admin=0):
    """
    add a user to database
    """
    # create engine, SQLite doesn't check the forgien key
    engine = sqlalchemy.create_engine(config_database_uri)

    # basic opration with session
    with orm.sessionmaker(engine)() as session:
        # organization operations
        plan_expire = datetime.datetime.now() + datetime.timedelta(days=365)
        organization = Organization(name="Test", plan_title="Free", plan_expire=plan_expire)

        session.add(organization)
        session.commit()
        print(session.query(Organization).all())

        # user operations
        _id = hashlib.md5(email.encode()).hexdigest()
        pwd = security.generate_password_hash(email)
        user = User(id=_id, pwd=pwd, admin=admin, email=email, organ_id=organization.id)

        session.add(user)
        session.commit()
        print(session.query(User).get(_id))


if __name__ == "__main__":
    init_db()
    add_user()
