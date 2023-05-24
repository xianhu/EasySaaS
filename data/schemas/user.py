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
    # is_admin: Optional[bool] = None
    # role_json: Optional[dict] = None


# used for request body
class UserCreate(BaseModel):
    email: EmailStr  # required
    password: str  # plain or hashed


# used for internal call
class UserCreatePri(UserCreate):
    id: Optional[int] = None
    name: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    email_verified: bool = False
    is_admin: bool = False
    role_json: dict = {}


# used for request body
class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[HttpUrl] = None


# used for internal call
class UserUpdatePri(UserUpdate):
    # id: Optional[int] = None
    # email: Optional[EmailStr] = None
    email_verified: Optional[bool] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    role_json: Optional[dict] = None
