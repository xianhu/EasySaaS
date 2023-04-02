# _*_ coding: utf-8 _*_

"""
tasks page
"""

import time

import dash
import feffery_antd_components as fac
from dash import html, Input, Output, State

TAG_BASE = "analysis"
TAG = "analysis-tasks"

# style of page
STYLE_PAGE = ""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    div_time = html.Div(id=f"id-{TAG}-div-time")
    div_output = html.Div(id=f"id-{TAG}-div-output")
    button_run = fac.AntdButton("Run Task", id=f"id-{TAG}-button-run")

    # return result
    return html.Div([button_run, div_time, div_output], className=None)


@dash.callback([
    Output(f"id-{TAG}-div-time", "children"),
    Output(f"id-{TAG}-div-output", "children"),
], [
    Input(f"id-{TAG}-button-run", "nClicks"),
    State(f"id-{TAG}-div-output", "children"),
], running=[
    (Output(f"id-{TAG}-button-run", "disabled"), True, False),
], progress=[
    Output(f"id-{TAG}-div-time", "children"),
    Output(f"id-{TAG}-div-output", "children"),
], background=True, prevent_initial_call=True)
def _update_page(set_progress, n_clicks, children):
    time_start = time.time()

    # run tasks
    out_children = "Output:"
    for index in range(10):
        time.sleep(1)
        time_run = time.time() - time_start

        # update progress
        out_children += f" {index}"
        set_progress([f"Time: {time_run}", out_children])

    # return result
    return f"Time(total): {time.time() - time_start}", dash.no_update
