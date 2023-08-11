# _*_ coding: utf-8 _*_

"""
admin api
"""

from fastapi import APIRouter

from . import file, user

# define router
router = APIRouter()
router.include_router(user.router, prefix="/user")
router.include_router(file.router, prefix="/file")
