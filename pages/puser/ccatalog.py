# _*_ coding: utf-8 _*_

"""
catalog component
"""

import dash_bootstrap_components as dbc
from dash import html

from ..paths import PATH_USER, PATH_LOGOUT

CATALOG_LIST = [
    ["ACCOUNT", None, [
        ("General", f"{PATH_USER}-general"),
        ("Security", f"{PATH_USER}-security"),
        ("Notifications", f"{PATH_USER}-notifications"),
    ]],
    ["BILLING", None, [
        ("Plan", f"{PATH_USER}-plan"),
        ("Payments", f"{PATH_USER}-payments"),
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
    catalog_children = []
    for title_first, icon_first, list_second in CATALOG_LIST:
        catalog_children.append(html.Div(title_first, className=class_first))

        for title_second, path in list_second:
            _class = "text-black hover-primary" if path != pathname else "text-white bg-primary"
            catalog_children.append(html.A(title_second, href=path, className=f"{class_second} {_class}"))
    catalog_children.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-4"))

    # return result
    return dbc.Card(catalog_children, class_name=class_name)
