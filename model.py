# _*_ coding: utf-8 _*_

"""
Model Defination
"""

import hashlib

import sqlalchemy
from sqlalchemy import func, orm
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security

from config import config_database_uri

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class User(app_db.Model):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(500), nullable=False)
    admin = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="0 or 1")

    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)

    plan_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("plans.id"))
    plan_expire = sqlalchemy.Column(sqlalchemy.Integer, default=-1, doc="day count")

    session = sqlalchemy.Column(sqlalchemy.String(500), doc="session value")
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="0 or 1")

    filename = sqlalchemy.Column(sqlalchemy.String(500), doc="file name")
    tempcol = sqlalchemy.Column(sqlalchemy.String(500), doc="temporary column")

    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now())

    # foreign key and relationship
    plan = orm.relationship("Plan", backref=orm.backref("users"))

    # print format
    def __repr__(self) -> str:
        col_list = [self.id, self.name, self.admin, self.email, self.phone]
        return f"User <{' - '.join(map(str, col_list))}>"


class Plan(app_db.Model):
    __tablename__ = "plans"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)

    content = sqlalchemy.Column(sqlalchemy.Text, doc="plan content")
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="plan price")

    pindex = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="plan index")
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="0 or 1")

    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now())

    # print format
    def __repr__(self) -> str:
        col_list = [self.id, self.name, self.price, self.pindex, self.status]
        return f"User <{' - '.join(map(str, col_list))}>"


def init_db():
    """
    initial database
    """
    # create engine, SQLite doesn't check the forgien key
    engine = sqlalchemy.create_engine(config_database_uri)

    # drop or create all tables
    app_db.Model.metadata.drop_all(engine)
    app_db.Model.metadata.create_all(engine)


def add_user(email="aaaa@qq.com", plan_id=None):
    """
    add a user to database
    """
    # create engine, SQLite doesn't check the forgien key
    engine = sqlalchemy.create_engine(config_database_uri)

    # basic opration with session
    with orm.sessionmaker(engine)() as session:
        _id = hashlib.md5(email.encode()).hexdigest()
        pwd = security.generate_password_hash(email)

        user = User(id=_id, pwd=pwd, admin=1, email=email, plan_id=plan_id)
        session.add(user)
        session.commit()

        print(session.query(User).get(_id))


if __name__ == "__main__":
    init_db()
    add_user()
