# _*_ coding: utf-8 _*_

"""
test models and schemas
"""

import logging

from pydantic import EmailStr

from core import security
from data import SessionMaker
from data.dmysql import init_db
from data.models import *
from data.schemas import *

# init db
init_db()

with SessionMaker() as session:
    # user info =========================================================================
    email = EmailStr("admin@easysaas.com")
    password = security.get_password_hash("a123456")

    # create user -- schemas of UserCreate and UserCreatePri
    user_schema = UserCreate(email=email, password=password)
    user_schema = UserCreatePri(id=100000, name="admin", **user_schema.dict(exclude_unset=True))

    # create user -- model of User
    user_model = User(**user_schema.dict(exclude_unset=True))
    session.add(user_model)
    session.commit()
    logging.warning(user_model.to_dict())

    # update user -- schemas of UserUpdate and UserUpdatePri
    user_schema = UserUpdate(name="admin", avatar="http://www.easysaas.com")
    system_role = {"role": "admin", "scopes": ["user:read", ]}
    user_schema = UserUpdatePri(system_role=system_role, **user_schema.dict(exclude_unset=True))
    [setattr(user_model, field, getattr(user_schema, field)) for field in user_schema]
    session.merge(user_model)
    session.commit()
    logging.warning(user_model.to_dict())

    # project info ======================================================================
    try:
        project = Project(name="test", desc="test")
        session.add(project)
        session.flush()

        user_project = UserProject(user_id=user_model.id, project_id=project.id)
        session.add(user_project)
        session.commit()
    except Exception as excep:
        logging.error(excep)
        session.rollback()
