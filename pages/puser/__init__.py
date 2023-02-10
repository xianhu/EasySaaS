# _*_ coding: utf-8 _*_

"""
user page
"""

import feffery_antd_components as fac
import flask_login
from dash import html, dcc

from .. import comps

TAG = "user"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # return layout
    return fac.AntdContent(children=[
        comps.get_component_header(None, user_title, dot=True),

        fac.AntdTabs(
            [
                fac.AntdTabPane(
                    html.Div(
                        '标签页1测试',

                    ),
                    tab='标签页1',
                    key='标签页1'
                ),
                fac.AntdTabPane(
                    html.Div(
                        fac.AntdButton('标签页2测试', type='primary'),

                    ),
                    tab='标签页2',
                    key='标签页2'
                ),
                fac.AntdTabPane(
                    html.Div(
                        fac.AntdButton('标签页3测试', type='dashed'),

                    ),
                    tab='标签页3',
                    key='标签页3'
                )
            ], className="w-75 m-auto mt-4"
        ),

        dcc.Store(id=f"id-{TAG}-store", data=dict(user_id=current_user.id)),
    ], className="vh-100 overflow-auto bg-main")
