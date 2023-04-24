# _*_ coding: utf-8 _*_

"""
project crud
"""

from .base import CRUDBase
from .. import Project
from ..schemas import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass


project = CRUDProject(Project)
