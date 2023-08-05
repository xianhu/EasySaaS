# _*_ coding: utf-8 _*_

"""
test data
"""

import logging
from pprint import pformat

from api.auth.utils import init_user_object
from core import get_password_hash
from data import SessionMaker
from data.models import FileTag
from data.schemas import UserCreateEmail, UserCreatePhone
from data.utils import init_db_tables

# init db with all tables
init_db_tables(model_list=None)

# init user with session
with SessionMaker() as session:
    pwd_hash = get_password_hash("a123456")

    # create user schema --------------------------------------------------------------------------
    email = "admin@easysaas.com"
    user_schema = UserCreateEmail(email=email, email_verified=True, password=pwd_hash)

    # initialize user object based on create schema
    _user_model = init_user_object(user_schema, session)
    logging.warning(pformat(_user_model.dict(), indent=2))

    # logging filetag models
    _filter = FileTag.user_id == _user_model.id
    for filetag_model in session.query(FileTag).filter(_filter).all():
        logging.warning("----%s", filetag_model.dict())

    # create user schema --------------------------------------------------------------------------
    phone = "+86-18675768543"
    user_schema = UserCreatePhone(phone=phone, phone_verified=True, password=pwd_hash)

    # initialize user object based on create schema
    _user_model = init_user_object(user_schema, session)
    logging.warning(pformat(_user_model.dict(), indent=2))

    # logging filetag models
    _filter = FileTag.user_id == _user_model.id
    for filetag_model in session.query(FileTag).filter(_filter).all():
        logging.warning("----%s", filetag_model.dict())
