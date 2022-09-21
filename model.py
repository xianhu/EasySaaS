# _*_ coding: utf-8 _*_

"""
Model Defination
"""

import hashlib

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, func, orm
from werkzeug import security

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class User(app_db.Model):
    __tablename__ = "users"
    __table_args__ = (
        Index("index_u_1", "name"),
        Index("index_u_2", "email"),
        Index("index_u_3", "phone"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(500), nullable=False)

    # informations
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)

    # company
    company_name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    company_avatar = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)

    # address
    addr_state = sqlalchemy.Column(sqlalchemy.String(50), doc="state of address")
    addr_city = sqlalchemy.Column(sqlalchemy.String(50), doc="city of address")
    addr_detail = sqlalchemy.Column(sqlalchemy.String(50), doc="detail of address")

    # others
    filename = sqlalchemy.Column(sqlalchemy.String(500), doc="file name")
    session = sqlalchemy.Column(sqlalchemy.String(500), doc="session value")
    tempcol = sqlalchemy.Column(sqlalchemy.String(500), doc="temporary column")

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="-1 0 1")
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now())

    # print format
    def __repr__(self) -> str:
        return f"User <{' - '.join(map(str, [self.id, self.name, self.email, self.phone]))}>"


def init_db(database_uri):
    """
    initial database
    """
    # create engine, SQLite doesn't check the forgien key
    engine = sqlalchemy.create_engine(database_uri)

    # drop or create all tables
    app_db.Model.metadata.drop_all(engine)
    app_db.Model.metadata.create_all(engine)
    return True


def test_db(database_uri):
    """
    add a user to database
    """
    # create engine, SQLite doesn't check forgien key
    engine = sqlalchemy.create_engine(database_uri)

    # basic opration with session
    with orm.sessionmaker(engine)() as session:
        # user operations
        email = "aaaa@qq.com"
        _id = hashlib.md5(email.encode()).hexdigest()
        pwd = security.generate_password_hash(email)
        user = User(id=_id, pwd=pwd, email=email)

        session.add(user)
        session.commit()
        print(session.query(User).get(_id))
    return True


if __name__ == "__main__":
    from config import config_database_uri

    init_db(config_database_uri)
    test_db(config_database_uri)
