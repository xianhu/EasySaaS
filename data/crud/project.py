# _*_ coding: utf-8 _*_

"""
crud of project
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Project  # Model
from ..schemas import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):

    def get_multi_of_user(self, session: Session, user_id: int, offset: int = 0, limit: int = 100) -> List[Project]:
        obj_model_list = session.query(Project).filter(
            Project.user_id == user_id,
        ).offset(offset).limit(limit).all()
        return obj_model_list

    def get_current_of_user(self, session: Session, user_id: int) -> Optional[Project]:
        obj_model = session.query(Project).filter(
            Project.user_id == user_id,
            Project.is_current == True,
        ).first()
        return obj_model

    def update_current_of_user(self, session: Session, user_id: int, project_id: int) -> bool:
        # update all projects
        session.query(Project).filter(
            Project.user_id == user_id,
        ).update({Project.is_current: False})
        # update current project
        session.query(Project).filter(
            Project.user_id == user_id,
            Project.id == project_id,
        ).update({Project.is_current: True})
        session.commit()
        return True


crud_project = CRUDProject(Project)
