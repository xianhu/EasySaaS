# _*_ coding: utf-8 _*_

"""
template of normal page
"""

import dash
from dash import Input, Output, MATCH, dcc, html


def layout(pathname, search, tag, children, class_name=None):
    """
    layout of template
    """
    # define components
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


# clientside callback
dash.clientside_callback(
    """
    function(href) {
        if (href != null && href != undefined) {
            window.location.href = href
        }
        return href
    }
    """,
    Output({"type": "id-address", "index": MATCH}, "data"),
    Input({"type": "id-address", "index": MATCH}, "href"),
    prevent_initial_call=True,
)
