# _*_ coding: utf-8 _*_

"""
models module
"""

from typing import Generator

import sqlalchemy.orm

from core.settings import settings
from .project import Project
from .user import User

# create engine and session_maker
engine = sqlalchemy.create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False, autoflush=True)


def get_db() -> Generator:
    """
    get db session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
