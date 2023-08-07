# _*_ coding: utf-8 _*_

"""
user api
"""

from fastapi import APIRouter

from . import code, stat, user

# define router
router = APIRouter()
router.include_router(user.router)
router.include_router(code.router)
router.include_router(stat.router)
