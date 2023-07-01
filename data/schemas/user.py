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
    # password: Optional[str] = None
    # system_admin: Optional[bool] = None
    # system_role: Optional[dict] = None


# used for request body
class UserCreate(BaseModel):
    email: EmailStr  # required
    password: str  # plain value


# used for request body
class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[HttpUrl] = None
