# _*_ coding: utf-8 _*_

"""
crud of user
"""

from typing import Optional

from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import User  # Model
from ..schemas import UserCreatePri, UserUpdatePri


class CRUDUser(CRUDBase[User, UserCreatePri, UserUpdatePri]):

    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        obj_model = session.query(User).filter(User.email == email).first()
        return obj_model


crud_user = CRUDUser(User)
