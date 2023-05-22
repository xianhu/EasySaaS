# _*_ coding: utf-8 _*_

"""
test models
"""

import logging

from core.utils import security
from data import SessionLocal
from data.crud import crud_project, crud_user
from data.dmysql import init_db
from data.schemas import ProjectCreate, ProjectCreatePri
from data.schemas import ProjectSchema
from data.schemas import ProjectUpdate, ProjectUpdatePri
from data.schemas import UserCreate, UserCreatePri
from data.schemas import UserSchema
from data.schemas import UserUpdate, UserUpdatePri

# init db
init_db()

with SessionLocal() as session:
    # user info =========================================================================
    email = "admin@easysaas.com"
    pwd_hash = security.get_pwd_hash("a123456")
    user_schema = UserCreate(email=email, password=pwd_hash)

    # create user -- UserCreatePri
    role_json = {"role": "admin", "permissions": ["*"]}
    user_schema = UserCreatePri(id=1001, role_json=role_json, **user_schema.dict(exclude_unset=True))
    user_model = crud_user.create(session, obj_schema=user_schema)
    logging.warning("create user: %s", user_model.to_dict())
    logging.warning("create user: %s", UserSchema(**user_model.to_dict()))

    # user info =========================================================================
    avatar = "https://www.example.com"
    user_schema = UserUpdate(name="admin", avatar=avatar)

    # update user -- UserUpdatePri
    user_schema = UserUpdatePri(email_verified=True, is_admin=True, **user_schema.dict(exclude_unset=True))
    user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)
    logging.warning("update user: %s", user_model.to_dict())
    logging.warning("update user: %s", UserSchema(**user_model.to_dict()))

    # project info ======================================================================
    user_id = user_model.id
    project_name = "demo project"
    project_schema = ProjectCreate(name=project_name, desc=None)

    # create project -- ProjectCreatePri
    project_schema = ProjectCreatePri(id=10001, user_id=user_id, **project_schema.dict(exclude_unset=True))
    project_model = crud_project.create(session, obj_schema=project_schema)
    logging.warning("create project: %s", project_model.to_dict())
    logging.warning("create project: %s", ProjectSchema(**project_model.to_dict()))

    # project info ======================================================================
    desc = "demo project description"
    project_schema = ProjectUpdate(desc=desc)

    # update project -- ProjectUpdatePri
    project_schema = ProjectUpdatePri(**project_schema.dict(exclude_unset=True))
    project_model = crud_project.update(session, obj_model=project_model, obj_schema=project_schema)
    logging.warning("update project: %s", project_model.to_dict())
    logging.warning("update project: %s", ProjectSchema(**project_model.to_dict()))

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
    logging.warning("delete project: %s\n", project_model.to_dict())
