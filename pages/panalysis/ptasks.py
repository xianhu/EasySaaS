# _*_ coding: utf-8 _*_

"""
tasks page
"""

import time

import dash
import feffery_antd_components as fac
from dash import Input, Output, html

TAG_BASE = "analysis"
TAG = "analysis-tasks"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        fac.AntdButton("Run Task", id=f"id-{TAG}-button-run"),
        html.Div(id=f"id-{TAG}-div-0"),
        html.Div(id=f"id-{TAG}-div-1"),
    ], className="vh-100 overflow-auto px-4 py-3")


@dash.callback(
    Output(f"id-{TAG}-div-0", "children"),
    Output(f"id-{TAG}-div-1", "children"),
    Input(f"id-{TAG}-button-run", "nClicks"),
    running=[
        (Output(f"id-{TAG}-button-run", "disabled"), True, False),
    ],
    progress=[
        Output(f"id-{TAG}-div-0", "children"),
        Output(f"id-{TAG}-div-1", "children"),
    ], background=True, prevent_initial_call=True)
def _update_page(set_progress, n_clicks):
    time_start = time.time()
    out_children = "Output:"

    # run tasks
    for index in range(10):
        time.sleep(1)
        time_run = time.time() - time_start

        # update progress
        out_children += f" {index}"
        set_progress([f"Time: {time_run}", out_children])

    # return result
    return f"Time(total): {time.time() - time_start}", dash.no_update
