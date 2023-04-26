# _*_ coding: utf-8 _*_

"""
project crud
"""

from typing import List

from sqlalchemy.orm import Session

from .base import CRUDBase
from .. import Project  # Model
from ..schemas import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):

    def get_multi_by_user(
            self, db: Session, user_id: int,
            offset: int = 0, limit: int = 100,
    ) -> List[Project]:
        obj_db_list = db.query(Project).filter(
            Project.user_id == user_id,
        ).offset(offset).limit(limit).all()
        return obj_db_list


project = CRUDProject(Project)
