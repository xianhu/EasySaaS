# _*_ coding: utf-8 _*_

"""
variables module
"""

from pydantic import constr

# define type of PhoneStr
PhoneStr = constr(pattern=r"^\+\d{1,3}-\d{7,15}$")

# define filetags of system
FILETAG_SYSTEM_SET = {"untagged", "favorite", "collect", "trash"}
