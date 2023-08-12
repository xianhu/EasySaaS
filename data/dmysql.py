# _*_ coding: utf-8 _*_

"""
database of mysql
"""

from typing import Generator

import sqlalchemy.orm
from sqlalchemy.orm import Session

from core import settings

# create engine and SessionMaker
engine = sqlalchemy.create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionMaker = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False)


def get_session() -> Generator[Session, None, None]:
    """
    generate session of mysql
    """
    with SessionMaker() as session:
        yield session
