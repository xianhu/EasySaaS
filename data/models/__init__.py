# _*_ coding: utf-8 _*_

"""
models module
-------------------------------------------------
User(N)  <-  UserProject  ->  Project(N)
-------------------------------------------------
User(1)  <-  FileTag(N)
                |
             FileTagFile
                |
User(1)  <-  File(N)
-------------------------------------------------
User(1)  <-  UserLog(N)
-------------------------------------------------
"""

from .file import File, FileTagFile
from .filetag import FileTag
from .project import Project, UserProject
from .user import User, UserLog
