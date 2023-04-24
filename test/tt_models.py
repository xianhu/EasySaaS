# _*_ coding: utf-8 _*_

"""
test models
"""

import logging

from core.security import get_password_hash
from models import Project, User, engine, get_db
from models.base import Model

# initialize database
Model.metadata.drop_all(engine, checkfirst=True)
Model.metadata.create_all(engine, checkfirst=True)

for db in get_db():
    # test user
    email = "admin@easysaas.com"
    user = User(pwd=get_password_hash("a123456"), email=email)
    db.add(user)
    db.commit()
    logging.warning("add user: %s", user.to_dict())

    # test project
    project_name = "demo project"
    project = Project(name=project_name, user_id=user.id)
    db.add(project)
    db.commit()
    logging.warning("add project: %s", project.to_dict())

    # test relationship
    logging.warning("user -> projects: %s", user.projects)
    logging.warning("project -> user: %s", project.user)
