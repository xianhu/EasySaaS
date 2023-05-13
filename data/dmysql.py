# _*_ coding: utf-8 _*_

"""
database of mysql
"""

from typing import Generator

import sqlalchemy.orm
from sqlalchemy.orm import Session

from core.settings import settings

# create engine and session_maker
engine = sqlalchemy.create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False, autoflush=True)


def get_session() -> Generator[Session, None, None]:
    """
    generate session of mysql
    """
    with SessionLocal() as session:
        yield session
