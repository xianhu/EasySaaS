# _*_ coding: utf-8 _*_

"""
test models and schemas
"""

from data import SessionMaker
from data.schemas import *
from data.utils import init_db_table, init_user_object
from core.security import get_password_hash

# init db
init_db_table()

with SessionMaker() as session:
    # user info -- email and password
    email, pwd_plain = "admin@easysaas.com", "a123456"
    user_schema = UserCreate(email=email, password=get_password_hash(pwd_plain))

    init_user_object(user_schema, session)

    #
    # # create user -- model of User
    # user_model = User(id=get_id_string(f"{email}-{time.time()}"),
    #                   email=user_schema.email,
    #                   password=get_password_hash(user_schema.password),
    #                   email_verified=True)
    # session.add(user_model)
    # session.commit()
    # logging.warning(user_model.dict())
    #
    # # logging user -- schema of User
    # user_schema = UserSchema(**user_model.dict())
    # logging.warning(user_schema.model_dump(exclude_unset=True))
    #
    # # update user -- schema of UserUpdate, model of User
    # user_schema = UserUpdate(avatar="https://example.com",
    #                          nickname="admin",
    #                          birthday=date(1989, 6, 6),
    #                          gender=1)
    # for field in user_schema.model_dump(exclude_unset=True):
    #     setattr(user_model, field, getattr(user_schema, field))
    # user_model.system_admin = True
    # user_model.system_role = {"scopes": ["user:read", ]}
    # session.merge(user_model)
    # session.commit()
    # logging.warning(user_model.dict())
    #
    # # logging user -- schema of User
    # user_schema = UserSchema(**user_model.dict())
    # logging.warning(user_schema.model_dump(exclude_unset=True))
    #
    # #  create filetag -- model of FileTag -- system
    # for filetag_name in FILETAG_SYSTEM_SET:
    #     filetag_id = get_id_string(f"{user_model.id}-{filetag_name}-{time.time()}")
    #     filetag_model = FileTag(id=filetag_id,
    #                             user_id=user_model.id,
    #                             name=filetag_name,
    #                             ttype="system")
    #     session.add(filetag_model)
    # session.commit()
    # logging.warning(user_model.filetags)
