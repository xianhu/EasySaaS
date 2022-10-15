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
        dbc.CardHeader("Change Password:", class_name="py-3"),
        dbc.CardBody("Change Password", class_name=None),
    ], class_name=class_name)
