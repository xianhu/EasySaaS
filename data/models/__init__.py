# _*_ coding: utf-8 _*_

"""
models module
Company(1)  <-  User(N)
User(1)     <-  Project(N)
User(1)     <-  FileTag(N)   <->  File(N)
"""

from .file import File, FileTag, FileTagFile
from .project import Project
from .user import Company, User
