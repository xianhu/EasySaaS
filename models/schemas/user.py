# _*_ coding: utf-8 _*_

"""
user schema
"""

from typing import Optional

from pydantic import EmailStr

from .base import UserBase


class UserSchema(UserBase):
    pass


class UserCreate(UserBase):
    pwd: str
    email: EmailStr


class UserUpdate(UserBase):
    pwd: Optional[str] = None


class UserInDB(UserBase):
    id: int
    pwd: str

    class Config:
        orm_mode = True
