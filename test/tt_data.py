# _*_ coding: utf-8 _*_

"""
test models and schemas
"""

import hashlib
import logging
import time
from datetime import date

from core import security
from data import SessionMaker
from data.dmysql import init_db
from data.models import *
from data.schemas import *

# init db
init_db()
# init_db(User)

with SessionMaker() as session:
    # user info -- email and password
    email, pwd_plain = "admin@easysaas.com", "a123456"
    user_schema = UserCreate(email=email, password=pwd_plain)

    # create user -- model of User
    user_model = User(id=hashlib.md5(f"{email}-{time.time()}".encode()).hexdigest(),
                      email=user_schema.email,
                      password=security.get_password_hash(user_schema.password),
                      email_verified=True)
    session.add(user_model)
    session.commit()
    logging.warning(user_model.dict())

    # logging user -- schema of User
    user_schema = UserSchema(**user_model.dict())
    logging.warning(user_schema.model_dump(exclude_unset=True))

    # update user -- schema of UserUpdate, model of User
    user_schema = UserUpdate(avatar="https://example.com",
                             nickname="admin",
                             birthday=date(1989, 6, 6),
                             gender=1)
    for field in user_schema.model_dump(exclude_unset=True):
        setattr(user_model, field, getattr(user_schema, field))
    user_model.system_admin = True
    user_model.system_role = {"scopes": ["user:read", ]}
    session.merge(user_model)
    session.commit()
    logging.warning(user_model.dict())

    # logging user -- schema of User
    user_schema = UserSchema(**user_model.dict())
    logging.warning(user_schema.model_dump(exclude_unset=True))
