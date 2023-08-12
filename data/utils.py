# _*_ coding: utf-8 _*_

"""
utility functions and constants
"""

from typing import Optional

from pydantic import constr

# define type of PhoneStr
PhoneStr = constr(pattern=r"^\+\d{1,3}-\d{7,15}$")

# define filetags of system
FILETAG_SYSTEM_SET = {"untagged", "favorite", "collect"}


def init_db_tables(model_list: Optional[list] = None) -> None:
    """
    initialize database or tables, only used for test
    :param model_list: model list, order by dependency
    """
    from .dmysql import engine
    from .models.base import Model
    if not model_list:
        Model.metadata.drop_all(engine, checkfirst=True)
        Model.metadata.create_all(engine, checkfirst=True)
        return None

    # drop models, create models
    for model in model_list[::-1]:
        model.__table__.drop(engine, checkfirst=True)
    for model in model_list:
        model.__table__.create(engine, checkfirst=True)
    return None
