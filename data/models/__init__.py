# _*_ coding: utf-8 _*_

"""
models module
User(N)  <-  UserProject  ->  Project(N)
User(1)  <-  FileTag(N)   <-  FileTagFile  ->  File(N)
"""

from .file import File, FileTag, FileTagFile
from .project import Project, UserProject
from .user import User
