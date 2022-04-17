# _*_ coding: utf-8 _*_

"""
constants
"""

import re

# regular of password、phone and email
RE_PWD = re.compile(r"^(?![0-9]+$)(?![a-zA-Z]+$)[\d\D]{6,20}$")
RE_PHONE = re.compile(r"^(13[0-9]|14[5|7]|15[0-9]|18[0-9])\d{8}$")
RE_EMAIL = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")

# page path
PATH_ROOT = "/"

PATH_INTROS = "/intros"
PATH_ANALYSIS = "/analysis"

PATH_LOGIN = "/login"
PATH_LOGOUT = "/logout"

PATH_REGISTERE = "/registere"
PATH_RESETPWDE = "/resetpwde"

PATH_USER = "/user"
PATH_ADMIN = "/admin"
