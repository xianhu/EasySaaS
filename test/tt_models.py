# _*_ coding: utf-8 _*_

"""
test models
"""

import logging

from core.utils import security
from data import SessionLocal, engine
from data.crud import crud_project, crud_user
from data.models import Model
from data.schemas import ProjectCreate, ProjectUpdate, ProjectUpdatePri
from data.schemas import UserCreate, UserUpdate, UserUpdatePri

# initialize database
Model.metadata.drop_all(engine, checkfirst=True)
Model.metadata.create_all(engine, checkfirst=True)

with SessionLocal() as db:
    # user info =========================================================================
    email = "admin@easysaas.com"
    pwd_hash = security.get_pwd_hash("a123456")

    # create user
    user_schema = UserCreate(id=1001, pwd=pwd_hash, email=email, email_verified=False)
    user_db = crud_user.create(db, obj_schema=user_schema)
    logging.warning("create user: %s", user_db.to_dict())

    # update user -- public
    user_schema = UserUpdate(name="admin")
    user_db = crud_user.update(db, obj_db=user_db, obj_schema=user_schema)
    logging.warning("update user [public]: %s", user_db.to_dict())

    # update user -- private
    user_schema = UserUpdatePri(pwd=pwd_hash, email_verified=True)
    user_db = crud_user.update(db, obj_db=user_db, obj_schema=user_schema)
    logging.warning("update user [private]: %s", user_db.to_dict())

    # project info ======================================================================
    user_id = user_db.id
    project_name = "demo project"

    # create project
    project_schema = ProjectCreate(id=10001, name=project_name, user_id=user_id)
    project_db = crud_project.create(db, obj_schema=project_schema)
    logging.warning("create project: %s", project_db.to_dict())

    # update project -- public
    project_schema = ProjectUpdate(desc="demo project description")
    project_db = crud_project.update(db, obj_db=project_db, obj_schema=project_schema)
    logging.warning("update project [public]: %s", project_db.to_dict())

    # update project -- private
    project_schema = ProjectUpdatePri(desc="demo project description - private")
    project_db = crud_project.update(db, obj_db=project_db, obj_schema=project_schema)
    logging.warning("update project [private]: %s", project_db.to_dict())

    # test relationship =================================================================
    logging.warning("user -> projects: %s", user_db.projects[0].to_dict())
    logging.warning("project -> user: %s", project_db.user.to_dict())

    # test get_multi ====================================================================
    user_db_list = crud_user.get_multi(db, offset=0, limit=100)
    project_db_list = crud_project.get_multi(db, offset=0, limit=100)
    logging.warning("user_db_list: %s", user_db_list)
    logging.warning("project_db_list: %s", project_db_list)

    # test delete =======================================================================
    project_db = crud_project.delete(db, _id=project_db.id)
    logging.warning("delete project: %s", project_db.to_dict())
