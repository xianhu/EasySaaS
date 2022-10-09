# _*_ coding: utf-8 _*_

"""
Change Password
"""

import dash_bootstrap_components as dbc

TAG = "user-infosec-pwd"


def layout(class_name=None):
    """
    layout of component
    """
    return dbc.Card(children=[
        dbc.CardHeader("Change Password:", class_name="px-4 py-3"),
        dbc.Row(children=[], align="center", class_name="p-4"),
    ], class_name=class_name)
