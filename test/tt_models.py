# _*_ coding: utf-8 _*_

"""
test models
"""

import logging

from core.security import get_password_hash
from models import DbMaker, engine
from models.base import Model
from models.crud import crud_project, crud_user
from models.schemas import ProjectCreate, ProjectUpdate
from models.schemas import UserCreate, UserUpdate

# initialize database
Model.metadata.drop_all(engine, checkfirst=True)
Model.metadata.create_all(engine, checkfirst=True)

with DbMaker() as db:
    # create user
    email = "admin@easysaas.com"
    user_schema = UserCreate(pwd=get_password_hash("a123456"), email=email, id=1001)
    user_db = crud_user.create(db, obj_schema=user_schema)
    logging.warning("create user: %s", user_db.to_dict())

    # update user by db
    user_db.name = "admin"
    user_db = crud_user.update(db, obj_db=user_db)
    logging.warning("update user: %s", user_db.to_dict())

    # update user by schema
    user_schema = UserUpdate(email_verified=True)
    user_db = crud_user.update_by_schema(db, obj_db=user_db, obj_schema=user_schema)
    logging.warning("update user: %s", user_db.to_dict())

    # create project
    project_name = "demo project"
    project_schema = ProjectCreate(name=project_name, user_id=user_db.id, id=10001)
    project_db = crud_project.create(db, obj_schema=project_schema)
    logging.warning("create project: %s", project_db.to_dict())

    # update project by db
    project_db.desc = "demo project description"
    project_db = crud_project.update(db, obj_db=project_db)
    logging.warning("update project: %s", project_db.to_dict())

    # update project by schema
    project_schema = ProjectUpdate(desc="demo project description")
    project_db = crud_project.update_by_schema(db, obj_db=project_db, obj_schema=project_schema)
    logging.warning("update project: %s", project_db.to_dict())

    # test relationship
    logging.warning("user -> projects: %s", user_db.projects)
    logging.warning("project -> user: %s", project_db.user)
