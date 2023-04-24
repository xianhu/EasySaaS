# _*_ coding: utf-8 _*_

"""
base schemas
"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    status: Optional[int] = 1


class ProjectBase(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    status: Optional[int] = 1
