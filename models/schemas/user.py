# _*_ coding: utf-8 _*_

"""
schemas of user
"""

from typing import Optional

from pydantic import EmailStr

from .base import UserBase


class UserSchema(UserBase):
    pass


class UserCreate(UserBase):
    email: EmailStr
    pwd: str


class UserUpdate(UserBase):
    pwd: str


class UserInDB(UserBase):
    id: Optional[int] = None
    pwd: Optional[str] = None

    class Config:
        orm_mode = True
