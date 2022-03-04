# _*_ coding: utf-8 _*_

"""
Model Defination
"""

import hashlib

from werkzeug import security
from flask_sqlalchemy import SQLAlchemy, sqlalchemy, orm

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class User(app_db.Model):
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

    filename = sqlalchemy.Column(sqlalchemy.String(500), doc="file name")

    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())

    # foreign key and relationship
    plan = orm.relationship("Plan", backref=orm.backref("users"))

    # print format
    def __repr__(self) -> str:
        return f"User <{self.id} - {self.name} - {self.email} - {self.phone} - {self.filename}>"


class Plan(app_db.Model):
    __tablename__ = "plans"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)

    content = sqlalchemy.Column(sqlalchemy.Text, doc="plan content")
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="plan price")

    pindex = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="plan index")
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="0 or 1")

    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())

    # print format
    def __repr__(self) -> str:
        return f"Plan <{self.id} - {self.name} - {self.price} - {self.pindex} - {self.status}>"


if __name__ == "__main__":
    from config import config_database_uri

    # create engine, SQLITE doesn't check the forgien key
    engine = sqlalchemy.create_engine(config_database_uri)

    # drop or create all tables
    app_db.Model.metadata.drop_all(engine)
    app_db.Model.metadata.create_all(engine)

    # basic opration with session
    with orm.sessionmaker(engine)() as session:
        plan = Plan(name="Free", content="for test")
        session.add(plan)
        session.commit()

        email = "aaaa@qq.com"
        _id = hashlib.md5(email.encode()).hexdigest()
        pwd = security.generate_password_hash(email)

        user = User(id=_id, pwd=pwd, email=email, plan_id=plan.id)
        session.add(user)
        session.commit()

        print(f"{plan}\n{plan.users}")
        print(session.query(User).get(_id))
