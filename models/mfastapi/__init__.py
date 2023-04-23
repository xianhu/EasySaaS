# _*_ coding: utf-8 _*_

"""
models in fastapi
"""

import sqlalchemy.orm

from core.settings import settings

engine = sqlalchemy.create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False)
