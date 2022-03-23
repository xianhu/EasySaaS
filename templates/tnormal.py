# _*_ coding: utf-8 _*_

"""
template of normal page
"""

from dash import dcc, html


def layout(pathname, search, tag, children, class_name=None):
    """
    layout of template
    """
    fixed_list = [
        html.A(id={"type": "id-address", "index": tag}),
        dcc.Store(id=f"id-{tag}-pathname", data=pathname),
        dcc.Store(id=f"id-{tag}-search", data=search),
    ]

    # return result
    if not isinstance(children, list):
        return html.Div([children, *fixed_list], className=class_name)
    else:
        return html.Div([*children, *fixed_list], className=class_name)
