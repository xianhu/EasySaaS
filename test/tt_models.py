# _*_ coding: utf-8 _*_

"""
test models
"""

import logging

from core.security import get_password_hash
from models import Project, User, engine, get_db
from models.base import Model
from models.schemas import UserCreate
from models.crud import curd_user

# initialize database
Model.metadata.drop_all(engine, checkfirst=True)
Model.metadata.create_all(engine, checkfirst=True)

for db in get_db():
    # test user
    email = "admin@easysaas.com"
    user = UserCreate(email=email, pwd=get_password_hash("a123456"))
    user_db = curd_user.create(db, obj_in=user)
    logging.warning("add user: %s", user_db.to_dict())
    #
    # # test project
    # project_name = "demo project"
    # project = Project(name=project_name, user_id=user.id)
    # db.add(project)
    # db.commit()
    # logging.warning("add project: %s", project.to_dict())
    #
    # # test relationship
    # logging.warning("user -> projects: %s", user.projects)
    # logging.warning("project -> user: %s", project.user)
