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
# app.layout = html.Div(children=[
#     dbc.Accordion(
#         [
#             dbc.AccordionItem(
#                 "This is the content of the first section", title="Item 1"
#             ),
#             dbc.AccordionItem(
#                 "This is the content of the second section", title="Item 2"
#             ),
#             dbc.AccordionItem(
#                 "This is the content of the third section", title="Item 3"
#             ),
#         ],
#         flush=True, active_item=None, id="id-a"
#     ),

#     dbc.Accordion(
#         [
#             dbc.AccordionItem(
#                 "This is the content of the first section", title="Item 1"
#             ),
#             dbc.AccordionItem(
#                 "This is the content of the second section", title="Item 2"
#             ),
#             dbc.AccordionItem(
#                 "This is the content of the third section", title="Item 3"
#             ),
#         ],
#         flush=True, active_item=None, id="id-b"
#     )

# ], className="w-25"
# )

app.layout = html.Div(children=[
    html.Div(children=[
        html.H2(children=[
            html.Button(children=[
                html.I(className="bi bi-house-door fs-5 me-1"),
                "Accordion Item #1"
            ], className="accordion-button collapsed", type="button", **{
                "data-bs-toggle": "collapse",
                "data-bs-target": "#flush-collapseOne",
                "aria-expanded": "false",
                "aria-controls": "flush-collapseOne"}
            )
        ], className="accordion-header", id="flush-headingOne"),

        html.Div(html.Div(children=[
            "1111111111",
        ], className="accordion-body"), id="flush-collapseOne", className="accordion-collapse collapse", **{
            "aria-labelledby": "flush-headingOne",
            "data-bs-parent": "#accordionFlushExample"}
        ),
    ], className="accordion-item"),

    html.Div(children=[
        html.H2(children=[
            html.Button(children=[
                html.I(className="bi bi-house-door fs-5 me-1"),
                "Accordion Item #1"
            ], className="accordion-button collapsed", type="button", **{
                "data-bs-toggle": "collapse",
                "data-bs-target": "#flush-collapseTwo",
                "aria-expanded": "false",
                "aria-controls": "flush-collapseTwo"}
            )
        ], className="accordion-header", id="flush-headingTwo"),

        html.Div(html.Div(children=[
            "2222222222",
        ], className="accordion-body"), id="flush-collapseTwo", className="accordion-collapse collapse", **{
            "aria-labelledby": "flush-headingTwo",
            "data-bs-parent": "#accordionFlushExample"}
        ),
    ], className="accordion-item"),


    html.Div(children=[
        html.H2(children=[
            html.Button(children=html.A([
                html.I(className="bi bi-house-door fs-5 me-1"),
                "Accordion Item #1"
            ], href="#", className="text-dark text-decoration-none"), className="accordion-button collapsed accordion-none bg-primary", type="button")
        ], className="accordion-header", id="flush-heading3"),

        # html.Div(html.Div(children=[
        #     "333333333",
        # ], className="accordion-body"), id="flush-collapse3", className="accordion-collapse collapse", **{
        #     "aria-labelledby": "flush-heading3",
        #     "data-bs-parent": "#accordionFlushExample"}
        # ),
    ], className="accordion-item"),


    html.Div(children=[
        html.H2(children=[
            html.Button(children=[
                html.I(className="bi bi-house-door fs-5 me-1"),
                "Accordion Item #1"
            ], className="accordion-button collapsed", type="button", **{
                "data-bs-toggle": "collapse",
                "data-bs-target": "#flush-collapse4",
                "aria-expanded": "false",
                "aria-controls": "flush-collapse4"}
            )
        ], className="accordion-header", id="flush-heading4"),

        html.Div(html.Div(children=[
            "2222222222",
        ], className="accordion-body"), id="flush-collapse4", className="accordion-collapse collapse", **{
            "aria-labelledby": "flush-heading4",
            # "data-bs-parent": "#accordionFlushExample"
            }
        ),
    ], className="accordion-item"),

], id="accordionFlushExample", className="accordion accordion-flush w-25")

# complete layout
app.validation_layout = dbc.Container([])


@app.callback(
    [Output("id-a", "active_item"),
     Output("id-b", "active_item"), ],
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
