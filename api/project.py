# _*_ coding: utf-8 _*_

"""
project api
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/list")
def project_list():
    """
    get project list
    """
    return {"message": "Hello World"}
