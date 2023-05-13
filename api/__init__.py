# _*_ coding: utf-8 _*_

"""
api module
"""

import logging

import sqlalchemy
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from data.dmysql import get_session
# from . import auth, project, user

# define api_router
api_router = APIRouter()
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(user.router, prefix="/user", tags=["user"])
# api_router.include_router(project.router, prefix="/project", tags=["project"])


@api_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_router.get("/test")
def test(session: Session = Depends(get_session)):
    session.execute(sqlalchemy.text("show tables;"))
    logging.warning("------")
    return {"message": "test"}
