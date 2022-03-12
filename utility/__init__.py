# _*_ coding: utf-8 _*_

"""
utility module
"""

import urllib.parse

from .consts import RE_PWD, RE_PHONE, RE_EMAIL
from .trigger import get_trigger_property


def parse_query_string(search):
    """
    parse query string: search
    """
    if (not search) or (not search.strip("?")):
        return {}
    return urllib.parse.parse_qs(search.strip("?"))
