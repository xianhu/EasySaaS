# _*_ coding: utf-8 _*_

"""
file api
"""

from fastapi import APIRouter

from . import file, link, updown

# define router
router = APIRouter()
router.include_router(file.router)
router.include_router(link.router)
router.include_router(updown.router)
