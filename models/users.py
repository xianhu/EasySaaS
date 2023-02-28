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

    # relationship
    projects = orm.relationship("Project", secondary="project_users", back_populates="users")

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

    # relationship
    users = orm.relationship("User", secondary="project_users", back_populates="projects")


class ProjectUser(BaseModel):
    __tablename__ = "project_users"

    # relationships
    user_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("users.id"), primary_key=True)
    project_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("projects.id"), primary_key=True)

    # informations
    role = sqlalchemy.Column(sqlalchemy.String(255), default="admin", doc="admin/member")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, doc="json of role")


def add_user(session, email, pwd=None, project_id=None, project_role="admin"):
    """
    add user, and add project-user relationship
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

    # add project-user relationship if necessary
    if project_id:
        project_user = ProjectUser(user_id=user.id, project_id=project_id, role=project_role)
        session.add(project_user)
        session.commit()

    # return
    return user


def add_project(session, name, desc=None, user_id=None, project_role="admin"):
    """
    add project, and add project-user relationship
    """
    # add project if necessary
    project = Project(id=get_md5(name + str(time.time())), name=name, desc=desc)
    session.add(project)
    session.commit()

    # add project-user relationship if necessary
    if user_id:
        project_user = ProjectUser(user_id=user_id, project_id=project.id, role=project_role)
        session.add(project_user)
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

    # create session and select data
    with orm.sessionmaker(engine)() as _session:
        _user = _session.query(User).get(_user_id)
        logging.warning("user.projects: %s", _user.projects)

        _project = _session.query(Project).get(_project_id)
        logging.warning("project.users: %s", _project.users)
