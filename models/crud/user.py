# _*_ coding: utf-8 _*_

"""
user crud
"""

from typing import Optional

from sqlalchemy.orm import Session

from .base import CRUDBase
from .. import User  # Model
from ..schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()


user = CRUDUser(User)
