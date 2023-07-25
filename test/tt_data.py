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

with SessionMaker() as session:
    # user info -- email and password
    email, pwd_plain = "admin@easysaas.com", "a123456"
    user_schema = UserCreate(email=email, password=get_password_hash(pwd_plain))

    # init user object
    user_model = init_user_object(user_schema, session)

    # logging user info
    logging.warning(user_model.dict())
    for filetag_model in user_model.filetags:
        logging.warning(filetag_model.dict())
