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
    pwd = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)

    # others columns
    token_verify = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)

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

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)

    # information
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

    # relationships: up.user, up.project
    user = orm.relationship("User", back_populates="user_projects")
    project = orm.relationship("Project", back_populates="user_projects")


if __name__ == "__main__":
    from config import CONFIG_DATABASE_URI
    from utility import get_md5

    # create engine
    engine = sqlalchemy.create_engine(CONFIG_DATABASE_URI)

    # initialize database
    BaseModel.metadata.drop_all(engine, checkfirst=True)
    BaseModel.metadata.create_all(engine, checkfirst=True)

    # =============================== test ===============================
    with orm.sessionmaker(engine)() as _session:
        _email = "admin@easysaas.com"
        _user = User(id=get_md5(_email), email=_email, status=1)
        _user.set_password_hash("a123456")
        _session.add(_user)
        _session.commit()
        logging.warning("add user: %s", _user.to_dict())

        _project_name = "demo project"
        _project = Project(id=get_md5(_project_name + str(time.time())), name=_project_name)
        _session.add(_project)
        _session.commit()
        logging.warning("add project: %s", _project.to_dict())

        _user_project = UserProject(user_id=_user.id, project_id=_project.id, role="admin")
        _session.add(_user_project)
        _session.commit()
        logging.warning("add user-project: %s", _user_project.to_dict())
