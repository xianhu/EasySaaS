# _*_ coding: utf-8 _*_

"""
filetag api
"""

from fastapi import APIRouter

from . import filetag

# define router
router = APIRouter()
router.include_router(filetag.router)
