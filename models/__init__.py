# _*_ coding: utf-8 _*_

"""
models module
"""

import logging
from typing import Generator

import sqlalchemy.orm
from sqlalchemy.orm import Session

from core.settings import settings
from .project import Project
from .user import User

# create engine and session_maker
engine = sqlalchemy.create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False, autoflush=True)


def get_db() -> Generator:
    """
    generate db session
    """
    try:
        db = SessionLocal()
        yield db
    except Exception as excep:
        logging.error("get_db: %s", excep)
        db = None
    return db.close() if db else None


class DbMaker(object):
    """
    with db session
    """

    def __enter__(self) -> Session:
        try:
            self.db = SessionLocal()
        except Exception as excep:
            logging.error("DbMaker: %s", excep)
            self.db = None
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close() if self.db else None
        return None
