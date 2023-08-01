# _*_ coding: utf-8 _*_

"""
utility functions
"""

from pydantic import constr

# define type of PhoneStr
PhoneStr = constr(pattern=r"^\+\d{1,3}-\d{7,15}$")

# define filetags of system
FILETAG_SYSTEM_SET = {"untagged", "favorite", "collect", "trash"}


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
