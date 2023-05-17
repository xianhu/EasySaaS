# _*_ coding: utf-8 _*_

"""
project api
"""

from fastapi import APIRouter, Depends

from data.models import User
from data.schemas import ProjectSchema
from .utils import get_current_user

# define router
router = APIRouter()


@router.post("/get", response_model=ProjectSchema)
def _get(current_user: User = Depends(get_current_user)):
    """
    get schema of project which is current
    """
    return 
