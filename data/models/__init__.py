# _*_ coding: utf-8 _*_

"""
models module
User(N)  <-  Project(N)
User(1)  <-  FileTag(N)  <->  File(N)
"""

from .file import File, FileTag, FileTagFile
from .project import Project, UserProject
from .user import User
