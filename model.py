# _*_ coding: utf-8 _*_

"""
Model Defination
"""

import datetime
import hashlib

import sqlalchemy
from sqlalchemy import ForeignKey, Index, func, orm
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class Organization(app_db.Model):
    __tablename__ = "organizations"
    __table_args__ = (
        Index("index_o_1", "name"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # informations
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)

    # address
    addr_state = sqlalchemy.Column(sqlalchemy.String(50), doc="state of address")
    addr_city = sqlalchemy.Column(sqlalchemy.String(50), doc="city of address")
    addr_detail = sqlalchemy.Column(sqlalchemy.String(50), doc="detail of address")

    # plan
    plan_title = sqlalchemy.Column(sqlalchemy.String(50), default="free")
    plan_expire = sqlalchemy.Column(sqlalchemy.DateTime, doc="expire datetime")

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="-1 0 1")
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now())

    # print format
    def __repr__(self) -> str:
        col_list = [self.id, self.name, self.plan_title, self.plan_expire, self.status]
        return f"Organization <{' - '.join(map(str, col_list))}>"


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
    isadmin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    # informations
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)

    # address
    addr_state = sqlalchemy.Column(sqlalchemy.String(50), doc="state of address")
    addr_city = sqlalchemy.Column(sqlalchemy.String(50), doc="city of address")
    addr_detail = sqlalchemy.Column(sqlalchemy.String(50), doc="detail of address")

    # others
    filename = sqlalchemy.Column(sqlalchemy.String(500), doc="file name")
    session = sqlalchemy.Column(sqlalchemy.String(500), doc="session value")
    tempcol = sqlalchemy.Column(sqlalchemy.String(500), doc="temporary column")

    # foreign key and relationship
    organ_role = sqlalchemy.Column(sqlalchemy.String(50), default="admin", doc="admin/staff")
    organ_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("organizations.id"))
    organization = orm.relationship("Organization", backref=orm.backref("users"), cascade="save-update")

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="-1 0 1")
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now())

    # print format
    def __repr__(self) -> str:
        col_list1 = [self.id, self.name, self.isadmin, self.email, self.phone]
        col_list2 = [self.addr_state, self.addr_city, self.addr_detail]
        col_list3 = [self.organization, self.organ_role, self.status]
        return f"User <{' - '.join(map(str, col_list1 + col_list2 + col_list3))}>"


class Notification(app_db.Model):
    __tablename__ = "notifications"
    __table_args__ = (
        Index("index_n_1", "creater"),
        Index("index_n_2", "level"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # informations
    creater = sqlalchemy.Column(sqlalchemy.String(50), doc="creater")
    level = sqlalchemy.Column(sqlalchemy.String(50), doc="normal/important")
    title = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="-1 0 1")
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now())

    # print format
    def __repr__(self) -> str:
        col_list = [self.id, self.creater, self.level, self.title, self.status]
        return f"Notification <{' - '.join(map(str, col_list))}>"


class NFDistribute(app_db.Model):
    __tablename__ = "nfdistributes"
    __table_args__ = (
        Index("index_nd_1", "user_id", "nf_id"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # foreign key and relationship
    user_id = sqlalchemy.Column(sqlalchemy.String(50), ForeignKey("users.id"))
    user = orm.relationship("User", backref=orm.backref("nfdistributes"), cascade="save-update")

    # foreign key and relationship
    nf_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("notifications.id"))
    notification = orm.relationship("Notification", backref=orm.backref("nfdistributes"), cascade="save-update")

    # is checked
    is_checked = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="True or False")

    # normal columns
    status = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="-1 0 1")
    datetime_create = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now())
    datetime_update = sqlalchemy.Column(sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now())

    # print format
    def __repr__(self) -> str:
        col_list = [self.id, self.user_id, self.nf_id, self.is_checked, self.status]
        return f"NFDistribute <{' - '.join(map(str, col_list))}>"


def init_db(database_uri):
    """
    initial database
    """
    # create engine, SQLite doesn't check the forgien key
    engine = sqlalchemy.create_engine(database_uri)

    # drop or create all tables
    app_db.Model.metadata.drop_all(engine)
    app_db.Model.metadata.create_all(engine)


def test_db(database_uri):
    """
    add a user to database
    """
    # create engine, SQLite doesn't check the forgien key
    engine = sqlalchemy.create_engine(database_uri)

    # basic opration with session
    with orm.sessionmaker(engine)() as session:
        # organization operations
        plan_expire = datetime.datetime.now() + datetime.timedelta(days=365)
        organization = Organization(name="Test", plan_title="free", plan_expire=plan_expire)

        session.add(organization)
        session.commit()
        print(session.query(Organization).all())

        # user operations
        email = "aaaa@qq.com"
        _id = hashlib.md5(email.encode()).hexdigest()
        pwd = security.generate_password_hash(email)
        user = User(id=_id, pwd=pwd, email=email, organ_id=organization.id)

        session.add(user)
        session.commit()
        print(session.query(User).get(_id))

        # test relationship
        print(organization.users)
        print(user.organization)

        # notification operations
        notification = Notification(creater="admin", level="normal", title="notify title")

        session.add(notification)
        session.commit()
        print(session.query(Notification).all())

        # notifycation distribute operations
        nfdistribute = NFDistribute(user_id=user.id, nf_id=notification.id)

        session.add(nfdistribute)
        session.commit()
        print(session.query(NFDistribute).all())

        # test relationship
        print(nfdistribute.user)
        print(user.nfdistributes)
        print(nfdistribute.notification)
        print(notification.nfdistributes)


if __name__ == "__main__":
    from config import config_database_uri

    init_db(config_database_uri)
    test_db(config_database_uri)
