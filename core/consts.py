# _*_ coding: utf-8 _*_

"""
constants definition
"""

import re

# regular of password、phone and email
RE_PWD = re.compile(r"^(?!\d+$)(?![a-zA-Z]+$)[\d\D]{6,20}$")
RE_PHONE = re.compile(r"^(13\d|14[5|7]|15\d|18\d)\d{8}$")
RE_EMAIL = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")

# format string of executejs
FMT_EXECUTEJS_HREF = "window.location.href = '{href}';"
FMT_EXECUTEJS_TITLE = "window.document.title = '{title}';"
