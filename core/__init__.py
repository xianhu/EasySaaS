# _*_ coding: utf-8 _*_

"""
core module
"""

import hashlib


def get_md5(source):
    """
    get md5 of source
    """
    str_encode = source.encode()
    return hashlib.md5(str_encode).hexdigest()
