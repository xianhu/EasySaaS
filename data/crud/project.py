# _*_ coding: utf-8 _*_

"""
crud of project
"""

from typing import List

from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Project  # Model
from ..schemas import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):

    def get_multi_by_user(self, session: Session, user_id: int, offset: int = 0, limit: int = 100) -> List[Project]:
        obj_model_list = session.query(Project).filter(Project.user_id == user_id).offset(offset).limit(limit).all()
        return obj_model_list


crud_project = CRUDProject(Project)