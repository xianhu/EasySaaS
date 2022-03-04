# _*_ coding: utf-8 _*_

"""
utility module
"""

import urllib.parse

from .trigger import get_trigger_property
from .consts import RE_PWD, RE_PHONE, RE_EMAIL


def parse_query_string(search):
    """
    parse query string: search
    """
    if (not search) or (not search.strip("?")):
        return {}
    search = search.strip("?")
    return urllib.parse.parse_qs(search)
