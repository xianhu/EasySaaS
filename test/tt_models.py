# _*_ coding: utf-8 _*_

"""
test models
"""

import logging

from core.security import get_password_hash
from models import engine, get_db
from models.base import Model
from models.crud import crud_project, crud_user
from models.schemas import ProjectCreate, ProjectUpdate
from models.schemas import UserCreate, UserUpdate

# initialize database
Model.metadata.drop_all(engine, checkfirst=True)
Model.metadata.create_all(engine, checkfirst=True)

for db in get_db():
    # test user
    email = "admin@easysaas.com"
    user_schema = UserCreate(email=email, pwd=get_password_hash("a123456"))
    user_db = crud_user.create(db, obj_schema=user_schema)
    logging.warning("add user: %s", user_db.to_dict())

    user_schema = UserUpdate(name="admin")
    user_db = crud_user.update(db, obj_db=user_db, obj_schema=user_schema)
    logging.warning("update user: %s", user_db.to_dict())

    # test project
    project_name = "demo project"
    project_schema = ProjectCreate(name=project_name, user_id=user_db.id)
    project_db = crud_project.create(db, obj_schema=project_schema)
    logging.warning("add project: %s", project_db.to_dict())

    project_schema = ProjectUpdate(desc="demo project description")
    project_db = crud_project.update(db, obj_db=project_db, obj_schema=project_schema)
    logging.warning("update project: %s", project_db.to_dict())

    # test relationship
    logging.warning("user -> projects: %s", user_db.projects)
    logging.warning("project -> user: %s", project_db.user)
