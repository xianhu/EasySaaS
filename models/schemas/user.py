# _*_ coding: utf-8 _*_

"""
user schema
"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = False


class UserCreate(UserSchema):
    pwd: str  # required
    email: EmailStr  # required
    email_verified: bool  # required


class UserUpdate(UserSchema):
    pwd: Optional[str] = None
