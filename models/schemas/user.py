# _*_ coding: utf-8 _*_

"""
user schema
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = False


class UserCreate(UserSchema):
    pwd: str  # required
    email: EmailStr  # required
    email_verified: bool  # required


class UserUpdate(UserSchema):
    email_verified: Optional[bool] = None

    class Config:
        fields = {"email": {"exclude": True}, "pwd": {"exclude": True}}
