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
        obj_db = db.query(User).filter(User.email == email).first()
        return obj_db

    def get_by_email_and_pwd(self, db: Session, email: str, pwd_hash: str) -> Optional[User]:
        obj_db = db.query(User).filter(User.email == email).first()
        return obj_db if obj_db.pwd == pwd_hash else None

    def update_email_verify(self, db: Session, email: str) -> User:
        obj_db = db.query(User).filter(User.email == email).first()
        obj_db.email_verify = True
        db.commit()
        return obj_db


user = CRUDUser(User)
