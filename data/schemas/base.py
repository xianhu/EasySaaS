# _*_ coding: utf-8 _*_

"""
base model
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from .. import PhoneStr

__all__ = [
    "date", "datetime", "Any", "Dict", "List", "Optional",
    "BaseModel", "Field", "EmailStr", "HttpUrl", "PhoneStr",
]
