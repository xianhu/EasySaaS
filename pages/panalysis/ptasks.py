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

# style of page
STYLE_PAGE = ""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        fac.AntdButton("Run Task", id=f"id-{TAG}-button-run"),
        html.Div(id=f"id-{TAG}-div-time"),
        html.Div(id=f"id-{TAG}-div-output"),
    ], className=None)


@dash.callback([
    Output(f"id-{TAG}-div-time", "children"),
    Output(f"id-{TAG}-div-output", "children"),
], [
    Input(f"id-{TAG}-button-run", "nClicks"),
], running=[
    (Output(f"id-{TAG}-button-run", "disabled"), True, False),
], progress=[
    Output(f"id-{TAG}-div-time", "children"),
    Output(f"id-{TAG}-div-output", "children"),
], progress_default=("-", "-"), background=True, prevent_initial_call=True)
def _update_page(set_progress, n_clicks):
    for i in range(10):
        set_progress([f"Time: {i}", f"Output: {i}"])
        time.sleep(1)
    return "Time: Done", "Output: Done"
