# _*_ coding: utf-8 _*_

"""
test data
"""

import logging

from api.auth.utils import init_user_object
from core.security import get_password_hash
from data import SessionMaker
from data.models import User
from data.schemas import UserCreateEmail, UserCreatePhone
from data.utils import init_db_tables

# init db
init_db_tables()

# init user with session
with SessionMaker() as session:
    pwd_hash = get_password_hash("a123456")

    # create user schema --------------------------------------------------------------------------
    email = "admin@easysaas.com"
    user_schema = UserCreateEmail(email=email, email_verified=True, password=pwd_hash)

    # initialize user object based on create schema
    _user_model1 = init_user_object(user_schema, session)

    # create user schema --------------------------------------------------------------------------
    phone = "+86-18675768543"
    user_schema = UserCreatePhone(phone=phone, phone_verified=True, password=pwd_hash)

    # initialize user object based on create schema
    _user_model2 = init_user_object(user_schema, session)

    # logging user and filetag models -------------------------------------------------------------
    for user_model in session.query(User).all():
        logging.warning(user_model.dict())
        for filetag_model in user_model.filetags:
            logging.warning("----%s", filetag_model.dict())
