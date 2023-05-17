# _*_ coding: utf-8 _*_

"""
project api
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from data import get_session
from data.crud import crud_project
from data.models import User
from data.schemas import ProjectCreate, ProjectSchema
from .utils import get_current_user

# define router
router = APIRouter()


@router.post("/create", response_model=ProjectSchema)
def _create(project_schema: ProjectCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    create project, and return schema of project
    """
    project_model = crud_project.create(session, obj_schema=project_schema)
    return ProjectSchema(**project_model.to_dict())


@router.get("/get", response_model=ProjectSchema)
def _get(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    get schema of project which is current
    """
    project_model = crud_project.get_current_of_user(session, user_id=current_user.id)
    return ProjectSchema(**project_model.to_dict())


@router.get("/get-multi", response_model=List[ProjectSchema])
def _get_multi(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    get schema of projects which belong to current_user
    """
    project_model_list = crud_project.get_multi_of_user(session, user_id=current_user.id)
    return [ProjectSchema(**project_model.to_dict()) for project_model in project_model_list]
