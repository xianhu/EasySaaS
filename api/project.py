# _*_ coding: utf-8 _*_

"""
project api
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import User
from models import get_db
from models.crud import crud_project
from models.schemas import ProjectSchema
from .utils import get_current_user

router = APIRouter()


@router.get("/list", response_model=List[ProjectSchema])
def _list(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    get project list
    """
    projects_list = crud_project.get_multi_by_user(db, user_id=current_user.id)
    return [project.to_dict() for project in projects_list]


@router.get("/{project_id}", response_model=ProjectSchema)
def _get_project(project_id: int, db: Session = Depends(get_db)):
    """
    get project's info
    """
    return crud_project.get(db, id=project_id).to_dict()
