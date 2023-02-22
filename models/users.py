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
    __table_args__ = (
        sqlalchemy.Index("index_pu_1", "user_id"),
        sqlalchemy.Index("index_pu_2", "project_id"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # relationships
    user_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("users.id"))
    project_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("projects.id"))

    # informations
    role = sqlalchemy.Column(sqlalchemy.String(255), default="admin", doc="admin/member")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, doc="json of role")


if __name__ == "__main__":
    from config import config_database_uri
    from utility import get_md5

    # create engine
    engine = sqlalchemy.create_engine(config_database_uri)

    # initialize database
    BaseModel.metadata.drop_all(engine, checkfirst=True)
    BaseModel.metadata.create_all(engine, checkfirst=True)

    # create session and add data
    _email = "admin@easysaas.com"
    with orm.sessionmaker(engine)() as session:
        _user = User(id=get_md5(_email), email=_email, name="admin")
        _user.set_password_hash("a123456")

        try:
            session.add(_user)
            session.commit()
            logging.warning("add user success: %s", _user.to_dict())
        except Exception as excep:
            logging.error("add user failed: %s", excep)
            session.rollback()
            exit()

    # create session and add data
    _project_name = "demo project"
    with orm.sessionmaker(engine)() as session:
        _user = session.query(User).filter(User.email == _email).first()

        _id = get_md5(_user.id + _project_name + str(time.time()))
        _project = Project(id=_id, name=_project_name, desc="demo project")
        _project_user = ProjectUser(user_id=_user.id, project_id=_project.id, role="admin")

        try:
            session.add_all([_project, _project_user])
            session.commit()
            logging.warning("add project success: %s", _project.to_dict())
            logging.warning("add project_user success: %s", _project_user.to_dict())
        except Exception as excep:
            logging.error("add project/project_user failed: %s", excep)
            session.rollback()
            exit()

    # create session and select data
    with orm.sessionmaker(engine)() as session:
        _user = session.query(User).filter(User.email == _email).first()
        logging.warning("user.projects: %s", _user.projects)

        _project = session.query(Project).filter(Project.name == _project_name).first()
        logging.warning("project.users: %s", _project.users)
