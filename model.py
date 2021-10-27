# _*_ coding: utf-8 _*_

"""
Model Defination
"""

import hashlib

from werkzeug import security
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy, sqlalchemy

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class User(app_db.Model, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(500), nullable=False)

    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)

    plan_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("plans.id"))
    plan_expire = sqlalchemy.Column(sqlalchemy.Integer, default=-1, doc="day count")

    session = sqlalchemy.Column(sqlalchemy.String(500), doc="session value")
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="0 or 1")

    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now())

    # foreign key and relationship
    plan = sqlalchemy.orm.relationship("Plan", backref=sqlalchemy.orm.backref("users"))

    # print format
    def __repr__(self) -> str:
        return f"User <{self.id} - {self.name} - {self.email} - {self.phone}>"


class Plan(app_db.Model):
    __tablename__ = "plans"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, doc="plan content")
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="0 or 1")

    price = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="plan price")
    pindex = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="plan index")

    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now())

    # print format
    def __repr__(self) -> str:
        return f"User <{self.id} - {self.name} - {self.status} - {self.price}>"


def init_db():
    """
    initial database
    """
    # create engine, SQLITE doesn't check the forgien key
    engine = sqlalchemy.create_engine(config_database_uri)

    # drop or create all tables
    app_db.Model.metadata.drop_all(engine)
    app_db.Model.metadata.create_all(engine)
    return


def test_db():
    """
    test database
    """
    # create Session class
    engine = sqlalchemy.create_engine(config_database_uri)
    DBSessinon = sqlalchemy.orm.sessionmaker(engine)

    # basic opration with session
    with DBSessinon() as session:
        plan = Plan(name="Free", content="for test")
        session.add(plan)
        session.commit()

        email = "aaaa@qq.com"
        _id = hashlib.md5(email.encode()).hexdigest()
        pwd = security.generate_password_hash(email)
        user1 = User(id=_id, pwd=pwd, email=email, plan_id=plan.id)
        session.add(user1)
        session.commit()
        print(session.query(User).get(_id))

        email = "bbbb@qq.com"
        _id = hashlib.md5(email.encode()).hexdigest()
        pwd = security.generate_password_hash(email)
        user2 = User(id=_id, pwd=pwd, email=email, plan_id=plan.id)
        session.merge(user2)
        session.commit()
        print(session.query(User).get(_id))

        user2.name = "user2"
        session.merge(user2)
        session.commit()
        print(session.query(User).get(_id))

        print(plan.users)
    return


if __name__ == "__main__":
    from config import config_database_uri
    init_db()
    test_db()
