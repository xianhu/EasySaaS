# _*_ coding: utf-8 _*_

"""
project api
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import User
from models import get_db
from models.crud import crud_project
from models.schemas import ProjectSchema
from .utils import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ProjectSchema])
def _get(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    get current_user's projects list
    """
    projects_list = crud_project.get_multi_by_user(db, user_id=current_user.id)
    return [project.to_dict() for project in projects_list]


@router.get("/{project_id}", response_model=ProjectSchema)
def _get_project(project_id: int, db: Session = Depends(get_db)):
    """
    get current_user's project based on project_id
    """
    project_db = crud_project.get(db, _id=project_id)
    if not (project_db and project_db.status == 1):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return ProjectSchema(**project_db.to_dict())


@router.post("/", response_model=ProjectSchema)
def _create(project_schema: ProjectSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    create project
    """
    project_db = crud_project.create(db, obj_schema=project_schema, user_id=current_user.id)
    return ProjectSchema(**project_db.to_dict())


@router.post("/update", response_model=ProjectSchema)
def _update(project_schema: ProjectSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    update project
    """
    project_db = crud_project.get(db, _id=project_schema.id)
    if not (project_db and project_db.status == 1):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    project_db = crud_project.update(db, obj_db=project_db, obj_schema=project_schema)
    return ProjectSchema(**project_db.to_dict())
