# _*_ coding: utf-8 _*_

"""
utility functions
"""

from .dmysql import engine
from .models.base import Model


def init_db(model=None) -> None:
    """
    initialize database
    """
    if not model:
        Model.metadata.drop_all(engine, checkfirst=True)
        Model.metadata.create_all(engine, checkfirst=True)
    else:
        model.__table__.drop(engine, checkfirst=True)
        model.__table__.create(engine, checkfirst=True)
    return None


def init_user(email, pwd_hash, session) -> None:
    """
    initialize user
    """
    user_id = get_id_string(f"{email}-{time.time()}")
    user_model = User(id=user_id, email=email, password=pwd_hash, email_verified=True)
    session.add(user_model)

    for filetag_name in FILETAG_SYSTEM_SET:
        filetag_id = get_id_string(f"{user_model.id}-{filetag_name}-{time.time()}")
        filetag_model = FileTag(id=filetag_id,
                                user_id=user_model.id,
                                name=filetag_name,
                                ttype="system")
        session.add(filetag_model)

    session.commit()
