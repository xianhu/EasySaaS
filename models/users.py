# _*_ coding: utf-8 _*_

"""
user model
"""

import logging
import time

import sqlalchemy
from sqlalchemy import orm
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

    # relationship: user.user_projects
    user_projects = orm.relationship("UserProject", back_populates="user")

    def check_password_hash(self, password):
        """
        check password hash
        """
        return security.check_password_hash(self.pwd, password)

    def set_password_hash(self, password):
        """
        set password hash
        """
        self.pwd = security.generate_password_hash(password)
        return self


class Project(BaseModel):
    __tablename__ = "projects"
    __table_args__ = (
        sqlalchemy.Index("index_p_1", "name"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)

    # informations
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)

    # informations
    ts_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ts_expired = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    # relationship: project.user_projects
    user_projects = orm.relationship("UserProject", back_populates="project")


class UserProject(BaseModel):
    __tablename__ = "user_projects"

    # relationships
    user_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("users.id"), primary_key=True)
    project_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("projects.id"), primary_key=True)

    # role and role_json of project
    role = sqlalchemy.Column(sqlalchemy.String(255), default="admin", doc="admin/writer/reader")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, doc="json of role")

    # relationships: user_projects.user, user_projects.project
    user = orm.relationship("User", back_populates="user_projects")
    project = orm.relationship("Project", back_populates="user_projects")


def add_user(session, email, pwd=None, project_id=None, project_role="admin"):
    """
    add user, and add user-project relationship if necessary
    """
    # add user if necessary, or update password
    user = session.query(User).filter(User.email == email).first()
    if not user:
        user = User(id=get_md5(email), email=email)
        user.set_password_hash(pwd)
        session.add(user)
        session.commit()
    elif pwd:
        user.set_password_hash(pwd)
        session.commit()

    # add user-project relationship if necessary
    if project_id:
        user_project = UserProject(user_id=user.id, project_id=project_id, role=project_role)
        session.add(user_project)
        session.commit()

    # return
    return user


def add_project(session, name, desc=None, user_id=None, project_role="admin"):
    """
    add project, and add user-project relationship
    """
    # add project if necessary
    project = Project(id=get_md5(name + str(time.time())), name=name, desc=desc)
    session.add(project)
    session.commit()

    # add user-project relationship if necessary
    if user_id:
        user_project = UserProject(user_id=user_id, project_id=project.id, role=project_role)
        session.add(user_project)
        session.commit()

    # return
    return project


if __name__ == "__main__":
    from config import config_database_uri
    from utility import get_md5

    # create engine
    engine = sqlalchemy.create_engine(config_database_uri)

    # initialize database
    BaseModel.metadata.drop_all(engine, checkfirst=True)
    BaseModel.metadata.create_all(engine, checkfirst=True)

    # =============================== test ===============================
    # create session and add data
    _email = "test1@easysaas.com"
    with orm.sessionmaker(engine)() as _session:
        _user = add_user(_session, _email, "a123456")
        logging.warning("add user: %s", _user.to_dict())

    # create session and add data
    _email = "admin@easysaas.com"
    with orm.sessionmaker(engine)() as _session:
        _user = add_user(_session, _email, "a123456")
        logging.warning("add user: %s", _user.to_dict())
    _user_id = _user.id

    # create session and add data
    _project_name = "demo project"
    with orm.sessionmaker(engine)() as _session:
        _project = add_project(_session, _project_name, user_id=_user_id)
        logging.warning("add project: %s", _project.to_dict())
    _project_id = _project.id

    # =============================== test ===============================
    # create session and select data
    with orm.sessionmaker(engine)() as _session:
        _user = _session.query(User).get(_user_id)
        logging.warning("get user: %s", _user.to_dict())
        for up in _user.user_projects:
            logging.warning("\tuser-project: %s", up.to_dict())
            logging.warning("\tproject: %s", up.project.to_dict())

        _project = _session.query(Project).get(_project_id)
        logging.warning("get project: %s", _project.to_dict())
        for up in _project.user_projects:
            logging.warning("\tuser-project: %s", up.to_dict())
            logging.warning("\tuser: %s", up.user.to_dict())
