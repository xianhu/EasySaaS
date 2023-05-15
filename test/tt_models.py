# _*_ coding: utf-8 _*_

"""
test models
"""

import logging

from core.utils import security
from data import SessionLocal
from data.crud import crud_project, crud_user
from data.dmysql import init_db
from data.schemas import ProjectCreate, ProjectUpdate
from data.schemas import UserCreate, UserUpdate, UserUpdatePri

# initialize database
init_db()

with SessionLocal() as session:
    # user info =========================================================================
    email = "admin@easysaas.com"
    pwd_hash = security.get_pwd_hash("a123456")

    # create user
    user_schema = UserCreate(id=1001, pwd=pwd_hash, email=email, email_verified=False)
    user_model = crud_user.create(session, obj_schema=user_schema)
    logging.warning("create user: %s", user_model.to_dict())

    # update user -- public
    user_schema = UserUpdate(name="admin-t", email_verified=True)
    user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)
    logging.warning("update user [public]: %s", user_model.to_dict())

    # update user -- private
    user_schema = UserUpdatePri(name="admin", email_verified=True)
    user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)
    logging.warning("update user [private]: %s", user_model.to_dict())

    # project info ======================================================================
    user_id = user_model.id
    project_name = "demo project"

    # create project
    project_schema = ProjectCreate(id=10001, name=project_name, user_id=user_id)
    project_model = crud_project.create(session, obj_schema=project_schema)
    logging.warning("create project: %s", project_model.to_dict())

    # update project
    project_schema = ProjectUpdate(desc="demo project description")
    project_model = crud_project.update(session, obj_model=project_model, obj_schema=project_schema)
    logging.warning("update project: %s", project_model.to_dict())

    # test relationship =================================================================
    logging.warning("user -> projects: %s", user_model.projects[0].to_dict())
    logging.warning("project -> user: %s", project_model.user.to_dict())

    # test get_multi ====================================================================
    user_model_list = crud_user.get_multi(session, offset=0, limit=100)
    logging.warning("user_model_list: %s", user_model_list)
    project_model_list = crud_project.get_multi(session, offset=0, limit=100)
    logging.warning("project_model_list: %s", project_model_list)

    # test delete =======================================================================
    project_model = crud_project.delete(session, _id=project_model.id)
    logging.warning("delete project: %s", project_model.to_dict())
