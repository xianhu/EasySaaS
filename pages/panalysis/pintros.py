# _*_ coding: utf-8 _*_

"""
intros page
"""

import random

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, ClientsideFunction, dcc, html

TAG = "analysis-intros"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define data
    chart_data = dict(
        id_chart_div=f"id-{TAG}-chart-div",
        id_chart_click=f"id-{TAG}-chart-click",
        x_data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        y_data=[random.randint(50, 100) for _ in range(10)],
    )

    # return result
    return html.Div(children=[
        html.Div(id=f"id-{TAG}-message"),
        html.Div(id=f"id-{TAG}-chart-div", style={"height": "500px"}),
        dcc.Store(id=f"id-{TAG}-chart-data", data=chart_data),
        fuc.FefferySessionStorage(id=f"id-{TAG}-chart-click"),
    ], className=None)


# client side callback
dash.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="render_chart",
    ),
    Output(f"id-{TAG}-chart-div", "children"),
    Input(f"id-{TAG}-chart-data", "data"),
)


@dash.callback(
    Output(f"id-{TAG}-message", "children"),
    Input(f"id-{TAG}-chart-click", "data"),
    prevent_initial_call=True,
)
def _display_message(chart_data_click):
    content = f"click: {chart_data_click}"
    return fac.AntdMessage(content=content, top=50)
