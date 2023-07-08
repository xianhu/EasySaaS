# _*_ coding: utf-8 _*_

"""
test models and schemas
"""

import logging

from core import security
from data import SessionMaker
from data.dmysql import init_db
from data.models import *
from data.schemas import *

# init db
init_db()

with SessionMaker() as session:
    # user info -- email and password
    email, pwd_plain = "admin@easysaas.com", "a123456"
    user_schema = UserCreate(email=email, password=pwd_plain)

    # create user -- model of User
    pwd_hash = security.get_password_hash(user_schema.password)
    user_model = User(id=100000, email=email, password=pwd_hash)
    session.add(user_model)
    session.commit()
    logging.warning(user_model.dict())

    # logging user -- schema of User
    user_schema = UserSchema(**user_model.dict())
    logging.warning(user_schema.model_dump(exclude_unset=True))

    # update user -- schema of UserUpdate, model of User
    user_schema = UserUpdate(nickname="admin", avatar="https://example.com")
    for field in user_schema.model_dump(exclude_unset=True):
        setattr(user_model, field, getattr(user_schema, field))
    user_model.email_verified = True
    user_model.system_admin = True
    user_model.system_role = {"scopes": ["user:read", ]}
    session.merge(user_model)
    session.commit()
    logging.warning(user_model.dict())

    # logging user -- schema of User
    user_schema = UserSchema(**user_model.dict())
    logging.warning(user_schema.model_dump(exclude_unset=True))
