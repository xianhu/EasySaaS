# _*_ coding: utf-8 _*_

"""
catalog component
"""

import dash_bootstrap_components as dbc
from dash import html

from . import paccount, pbilling
from ..paths import PATH_USER, PATH_LOGOUT

CATALOG_LIST = [
    ["ACCOUNT", None, [
        ("General", f"{PATH_USER}-general", paccount),
        ("Security", f"{PATH_USER}-security", paccount),
        ("Notifications", f"{PATH_USER}-notifications", paccount),
    ]],
    ["BILLING", None, [
        ("Plan", f"{PATH_USER}-plan", pbilling),
        ("Payments", f"{PATH_USER}-payments", pbilling),
    ]],
]


def layout(pathname, search, class_name=None):
    """
    layout of component
    """
    # define class
    class_first = "small text-muted mt-4 mb-2 px-4"
    class_second = "small text-decoration-none px-4 py-2"

    # define components
    catalog_items = []
    for title_first, icon_first, list_second in CATALOG_LIST:
        catalog_items.append(html.Div(title_first, className=class_first))

        for title_second, path, page in list_second:
            _class = "text-black hover-primary" if path != pathname else "text-white bg-primary"
            catalog_items.append(html.A(title_second, href=path, className=f"{class_second} {_class}"))

    # define components
    catalog_items.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-4"))

    # return result
    return dbc.Card(catalog_items, class_name=class_name)


def content(pathname, search):
    """
    content of catalog item
    """
    # define pathname, title and content
    for title_first, icon_first, list_second in CATALOG_LIST:
        for title_second, path, page in list_second:
            if path != pathname:
                continue

            # return result
            pathname, title = path, title_first
            return pathname, title, page.layout(pathname, search)

    # return default result
    pathname, title = f"{PATH_USER}-general", "ACCOUNT"
    return pathname, title, paccount.layout(pathname, search)
