# _*_ coding: utf-8 _*_

"""
user schema
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


# used for response_model
class UserSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = None


# used for internal call
class UserCreate(UserSchema):
    email: EmailStr  # required
    email_verified: bool  # required
    password: str  # required
    is_admin: bool = False  # default


# used for request body
class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[HttpUrl] = None


# used for internal call
class UserUpdatePri(UserUpdate):
    # email: Optional[EmailStr] = None
    email_verified: Optional[bool] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
