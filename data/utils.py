# _*_ coding: utf-8 _*_

"""
utility functions
"""

import time

from sqlalchemy.orm import Session

from core.utils import get_id_string
from .models import FileTag, User
from .schemas import FileTagCreate, UserCreate
from .vars import FILETAG_SYSTEM_SET


def init_db_table(model=None) -> None:
    """
    initialize database or table
    """
    from .dmysql import engine
    from .models.base import Model
    if not model:
        Model.metadata.drop_all(engine, checkfirst=True)
        Model.metadata.create_all(engine, checkfirst=True)
    else:
        model.__table__.drop(engine, checkfirst=True)
        model.__table__.create(engine, checkfirst=True)
    return None


def init_user_object(user_schema: UserCreate, session: Session) -> User:
    """
    initialize user object based on create schema
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
