# _*_ coding: utf-8 _*_

"""
constants
"""

import re

# regular of email and password
RE_PWD = re.compile(r"^(?![0-9]+$)(?![a-zA-Z]+$)[\d\D]{6,20}$")
RE_EMAIL = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
