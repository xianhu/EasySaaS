# _*_ coding: utf-8 _*_

"""
user schema
"""

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
    id: int
    pwd: str

    class Config:
        orm_mode = True
