# _*_ coding: utf-8 _*_

"""
intros page
"""

import random

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, ClientsideFunction, dcc, html

TAG_BASE = "analysis"
TAG = "analysis-intros"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define data
    chart_data = dict(
        id_chart_div=f"id-{TAG}-chart-div",  # show chart
        id_chart_click=f"id-{TAG}-chart-click",  # store click data
        x_data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        y_data=[random.randint(50, 100) for _ in range(10)],
    )

    # return result
    style = {"height": "500px"}
    return html.Div(children=[
        html.Div(id=f"id-{TAG}-chart-div", style=style),  # show chart
        fuc.FefferySessionStorage(id=f"id-{TAG}-chart-click"),  # store click data
        dcc.Store(id=f"id-{TAG}-chart-data", data=chart_data),  # trigger clientside callback
        html.Div(id=f"id-{TAG}-message"),
    ], className=None)


# client side callback
dash.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="render_chart",
    ),
    Output(f"id-{TAG}-chart-div", "children"),
    Input(f"id-{TAG}-chart-data", "data"),
    prevent_initial_call=False,
)


@dash.callback(
    Output(f"id-{TAG}-message", "children"),
    Input(f"id-{TAG}-chart-click", "data"),
    prevent_initial_call=True,
)
def _update_page(chart_click_data):
    content = f"click: {chart_click_data}"
    return fac.AntdMessage(content=content, top=50)
