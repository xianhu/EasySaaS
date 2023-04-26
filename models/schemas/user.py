# _*_ coding: utf-8 _*_

"""
user schema
"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = False
    status: Optional[int] = 1


class UserCreate(UserSchema):
    pwd: str
    email: EmailStr


class UserUpdate(UserSchema):
    pwd: Optional[str] = None
    # email_verified: Optional[bool]
