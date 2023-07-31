# _*_ coding: utf-8 _*_

"""
auth api
"""

from fastapi import APIRouter

from . import auth, code

# define router
router = APIRouter()

# include router
router.include_router(auth.router)
router.include_router(code.router)
