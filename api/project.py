# _*_ coding: utf-8 _*_

"""
project api
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.settings import error_tips
from data import get_session
from data.crud import crud_project
from data.models import User
from data.schemas import ProjectCreate, ProjectCreatePri
from data.schemas import ProjectSchema
from data.schemas import ProjectUpdate, ProjectUpdatePri
from .utils import get_current_user

# define router
router = APIRouter()


@router.post("/create", response_model=ProjectSchema)
def _create(project_schema: ProjectCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    create project, and return schema of project
    """
    user_id = current_user.id
    project_dict = project_schema.dict(exclude_unset=True)

    # create project based on ProjectCreatePri
    project_schema = ProjectCreatePri(user_id=user_id, **project_dict)
    project_model = crud_project.create(session, obj_schema=project_schema)

    # update current project of user and refresh project_model
    crud_project.update_current_of_user(session, user_id=user_id, project_id=project_model.id)
    project_model = crud_project.get(session, _id=project_model.id)

    # return ProjectSchema
    return ProjectSchema(**project_model.to_dict())


@router.get("/get", response_model=ProjectSchema)
def _get(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    get schema of project which is current
    """
    user_id = current_user.id
    project_model = crud_project.get_current_of_user(session, user_id=user_id)
    return ProjectSchema(**project_model.to_dict())


@router.get("/get-multi", response_model=List[ProjectSchema])
def _get_multi(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    get schema of projects which belong to current_user
    """
    user_id = current_user.id
    project_model_list = crud_project.get_multi_of_user(session, user_id=user_id)
    return [ProjectSchema(**project_model.to_dict()) for project_model in project_model_list]


@router.get("/get/{project_id}", response_model=ProjectSchema)
def _get_by_id(project_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    get schema of project by project_id
    """
    user_id = current_user.id
    project_model = crud_project.get(session, _id=project_id)
    if (not project_model) or (project_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_tips.QUERY_FAILED,
        )
    return ProjectSchema(**project_model.to_dict())


@router.post("/update", response_model=ProjectSchema)
def _update(project_id: int, project_schema: ProjectUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    update project, and return schema of project
    """
    user_id = current_user.id

    # get project_model by project_id
    project_model = crud_project.get(session, _id=project_id)
    if (not project_model) or (project_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_tips.UPDATE_FAILED,
        )

    # update project based on ProjectUpdatePri
    project_schema = ProjectUpdatePri(**project_schema.dict(exclude_unset=True))
    project_model = crud_project.update(session, obj_model=project_model, obj_schema=project_schema)

    # return ProjectSchema
    return ProjectSchema(**project_model.to_dict())
