# _*_ coding: utf-8 _*_

"""
test data
"""

import logging

from core.security import get_password_hash
from data import SessionMaker
from data.schemas import UserCreate
from data.utils import init_db_table, init_user_object

# init db
init_db_table()

# init user with session
with SessionMaker() as session:
    # create user variables
    email, pwd_plain = "admin@easysaas.com", "a123456"
    user_schema = UserCreate(email=email, password=get_password_hash(pwd_plain))

    # initialize user object based on user schema
    user_model = init_user_object(user_schema, session)

    # logging user and filetag model
    logging.warning(user_model.dict())
    for filetag_model in user_model.filetags:
        logging.warning("\t%s", filetag_model.dict())
