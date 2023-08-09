# _*_ coding: utf-8 _*_

"""
test data
"""

import logging
from pprint import pformat

from api.utils import create_user_object  # noqa: F401
from core import get_password_hash
from data import SessionMaker
from data.models import File, FileTag, FileTagFile
from data.schemas import UserCreateEmail, UserCreatePhone
from data.utils import init_db_tables  # noqa: F401

# init db with all tables
init_db_tables(model_list=None)

# init tables by model list
init_db_tables(model_list=[FileTag, File, FileTagFile])

# init user with session
with SessionMaker() as session:
    pwd_hash = get_password_hash("a123456")

    # create user schema --------------------------------------------------------------------------
    email = "admin@easysaas.com"
    user_schema = UserCreateEmail(email=email, email_verified=True, password=pwd_hash,
                                  is_admin=True, role_json={"role": "admin"})

    # create user object based on create schema
    user_model = create_user_object(user_schema, session)
    logging.warning(pformat(user_model.dict(), indent=2))

    # logging filetag models
    filter0 = FileTag.user_id == user_model.id
    for filetag_model in session.query(FileTag).filter(filter0).all():
        logging.warning("----%s", filetag_model.dict())

    # create user schema --------------------------------------------------------------------------
    phone = "+86-18000000000"
    user_schema = UserCreatePhone(phone=phone, phone_verified=True, password=pwd_hash)

    # create user object based on create schema
    user_model = create_user_object(user_schema, session)
    logging.warning(pformat(user_model.dict(), indent=2))

    # logging filetag models
    filter0 = FileTag.user_id == user_model.id
    for filetag_model in session.query(FileTag).filter(filter0).all():
        logging.warning("----%s", filetag_model.dict())
