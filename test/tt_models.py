# _*_ coding: utf-8 _*_

"""
test models
"""

import logging

from core.utils import security
from models import DbMaker, engine
from models.base import Model
from models.crud import crud_project, crud_user
from models.schemas import ProjectCreate, ProjectUpdate
from models.schemas import UserCreate, UserUpdate

# initialize database
Model.metadata.drop_all(engine, checkfirst=True)
Model.metadata.create_all(engine, checkfirst=True)

with DbMaker() as db:
    # user info =========================================================================
    email = "admin@easysaas.com"
    pwd_hash = security.get_pwd_hash("a123456")

    # create user
    user_schema = UserCreate(id=1001, pwd=pwd_hash, email=email, email_verified=False)
    user_db = crud_user.create(db, obj_schema=user_schema)
    logging.warning("create user: %s", user_db.to_dict())

    # update user
    user_schema = UserUpdate(name="admin", email_verified=True)
    user_db = crud_user.update(db, obj_db=user_db, obj_schema=user_schema)
    logging.warning("update user: %s", user_db.to_dict())

    # project info ======================================================================
    user_id = user_db.id
    project_name = "demo project"

    # create project
    project_schema = ProjectCreate(id=10001, name=project_name, user_id=user_id)
    project_db = crud_project.create(db, obj_schema=project_schema)
    logging.warning("create project: %s", project_db.to_dict())

    # update project
    project_schema = ProjectUpdate(desc="demo project description")
    project_db = crud_project.update(db, obj_db=project_db, obj_schema=project_schema)
    logging.warning("update project: %s", project_db.to_dict())

    # test relationship =================================================================
    logging.warning("user -> projects: %s", user_db.projects)
    logging.warning("project -> user: %s", project_db.user)

    # test get_multi
    user_db_list = crud_user.get_multi(db, offset=0, limit=100)
    project_db_list = crud_project.get_multi(db, offset=0, limit=100)
