# _*_ coding: utf-8 _*_

"""
admin api
"""

from fastapi import APIRouter

from . import user

# define router
router = APIRouter()
router.include_router(user.router, prefix="/user")
