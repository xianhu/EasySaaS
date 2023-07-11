# _*_ coding: utf-8 _*_

"""
database of mysql
"""

from typing import Generator

import sqlalchemy.orm
from sqlalchemy.orm import Session

from core.settings import settings
from .models.base import Model

# create engine and SessionMaker
engine = sqlalchemy.create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionMaker = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False, autoflush=True)


def get_session() -> Generator[Session, None, None]:
    """
    generate session of mysql
    """
    with SessionMaker() as session:
        yield session


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
