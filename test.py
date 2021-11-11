# _*_ coding: utf-8 _*_

"""
Layout
"""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import app, server
from config import config_app_name

# app layout
app.title = config_app_name
app.layout = html.Div(children=[
    dbc.Accordion(
        [
            dbc.AccordionItem(
                "This is the content of the first section", title="Item 1"
            ),
            dbc.AccordionItem(
                "This is the content of the second section", title="Item 2"
            ),
            dbc.AccordionItem(
                "This is the content of the third section", title="Item 3"
            ),
        ],
        flush=True, active_item=None, id="id-a"
    ),

    dbc.Accordion(
        [
            dbc.AccordionItem(
                "This is the content of the first section", title="Item 1"
            ),
            dbc.AccordionItem(
                "This is the content of the second section", title="Item 2"
            ),
            dbc.AccordionItem(
                "This is the content of the third section", title="Item 3"
            ),
        ],
        flush=True, active_item=None, id="id-b"
    )

], className="w-25"
)

# complete layout
app.validation_layout = dbc.Container([])

@app.callback(
    [Output("id-a", "active_item"),
    Output("id-b", "active_item"),],
    [Input("id-a", "active_item"),
    Input("id-b", "active_item")],
)
def change_item(item1, item2):
    print(dash.callback_context.triggered)
    a = dash.callback_context.triggered[0]
    if str(a).find("id-a.active_item") > 0:
        return dash.no_update, None
    else:
        return None, dash.no_update


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8089, debug=True)
