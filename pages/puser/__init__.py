# _*_ coding: utf-8 _*_

"""
user page
"""

from ..comps import cfooter, cnavbar
from ..paths import *


def layout(pathname, search):
    """
    layout of page
    """
    fluid = None

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=fluid)
    footer = cfooter.layout(pathname, search, fluid=fluid)


    # return result
    return [navbar, "user", footer]
