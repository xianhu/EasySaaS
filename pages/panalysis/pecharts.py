# _*_ coding: utf-8 _*_

"""
echarts page
"""

import random

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import ClientsideFunction, Input, Output, dcc, html

TAG_BASE = "analysis"
TAG = "analysis-echarts"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define params
    params_chart = dict(
        # id_xxx of chart
        id_div=f"id-{TAG}-div-chart",  # div to show chart
        id_storage=f"id-{TAG}-storage-chart",  # storage of chart click data
        # data of chart
        x_data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        y_data=[random.randint(50, 100) for _ in range(10)],
    )

    # return result
    style = {"height": "500px"}
    return html.Div(children=[
        # define components
        html.Div(id=f"id-{TAG}-div-chart", style=style),  # div to show chart
        fuc.FefferySessionStorage(id=f"id-{TAG}-storage-chart"),  # storage of chart click data

        # params to trigger clientside callback
        dcc.Store(id=f"id-{TAG}-params-chart", data=params_chart),

        # message to show information
        html.Div(id=f"id-{TAG}-message-chart"),
    ], className="vh-100 overflow-auto px-4 py-3")


# trigger clientside callback
dash.clientside_callback(
    ClientsideFunction(
        namespace="ns_echarts",
        function_name="render_chart",
    ),
    Output(f"id-{TAG}-div-chart", "data"),
    Input(f"id-{TAG}-params-chart", "data"),
)


@dash.callback(
    Output(f"id-{TAG}-message-chart", "children"),
    Input(f"id-{TAG}-storage-chart", "data"),
    prevent_initial_call=True,
)
def _update_page(data_storage):
    content = f"click: {data_storage}"
    return fac.AntdMessage(content=content, top=50)
