# _*_ coding: utf-8 _*_

"""
utility module
"""

import urllib.parse

from .address import AddressAIO
from .consts import RE_PWD, RE_PHONE, RE_EMAIL
from .trigger import get_trigger_property


def parse_query_string(search):
    """
    parse query string: search
    """
    if (not search) or (search[0] != "?"):
        return {}
    search = search[1:].strip()
    return urllib.parse.parse_qs(search)


if __name__ == "__main__":
    print(parse_query_string("ignore"))
    print(parse_query_string("?a=1&b=2"))
    print(parse_query_string("?a=1&b=string"))
