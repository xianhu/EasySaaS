# _*_ coding: utf-8 _*_

"""
admin api
"""

from fastapi import APIRouter, Depends

from . import file, user
from ..utils import get_current_user_admin

# define router
router = APIRouter(dependencies=[Depends(get_current_user_admin), ])
router.include_router(user.router, prefix="/user")
router.include_router(file.router, prefix="/file")
