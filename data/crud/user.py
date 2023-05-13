# _*_ coding: utf-8 _*_

"""
user crud
"""

from typing import Optional

from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import User  # Model
from ..schemas import UserCreate, UserUpdate, UserUpdatePri


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate, UserUpdatePri]):

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        obj_db = db.query(User).filter(User.email == email).first()
        return obj_db


user = CRUDUser(User)
