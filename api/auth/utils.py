# _*_ coding: utf-8 _*_

"""
auth api
"""

import time
from enum import Enum
from typing import Optional

from pydantic import Field
from sqlalchemy.orm import Session

from core.utils import get_id_string
from data.models import FileTag, User
from data.schemas import FileTagCreate, Resp, UserCreate
from data.utils import FILETAG_SYSTEM_SET


# response model
class RespSend(Resp):
    token: Optional[str] = Field(None)


# enum of ttype
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


# enum of client_id
class ClientID(str, Enum):
    web = "web"
    ios = "ios"
    android = "android"


def init_user_object(user_schema: UserCreate, session: Session) -> User:
    """
    initialize user object based on create schema, return user model
    """
    try:
        # create user model based on create schema
        user_id = get_id_string(f"{user_schema.password}-{time.time()}")
        user_kwargs = user_schema.model_dump(exclude_unset=True)
        user_model = User(id=user_id, **user_kwargs)
        session.add(user_model)

        # create filetag model
        user_id = user_model.id
        for filetag_name in FILETAG_SYSTEM_SET:
            # create filetag_id and filetag schema
            filetag_id = get_id_string(f"{user_id}-{filetag_name}-{time.time()}")
            filetag_schema = FileTagCreate(name=filetag_name, icon="default", color="default")

            # create filetag model based on create schema, ttype="system"
            filetag_kwargs = filetag_schema.model_dump(exclude_unset=True)
            filetag_model = FileTag(id=filetag_id, user_id=user_id, **filetag_kwargs, ttype="system")
            session.add(filetag_model)

        # commit session
        session.commit()
        return user_model
    except Exception as excep:
        session.rollback()
        raise excep
