# _*_ coding: utf-8 _*_

"""
Invoice History
"""

import dash_bootstrap_components as dbc
from dash import html

TAG = "user-invoice"
INVOICE_LIST = [
    ("91240", "01/12/2020", 0),
    ("91230", "01/11/2020", 1),
    ("91220", "01/10/2020", 1),
    ("91210", "01/09/2020", 1),
]


def layout(pathname, search, class_name=None):
    """
    layout of card
    """
    # define components
    invoice_row_list = []
    for _id, _date, _flag in INVOICE_LIST:
        if len(invoice_row_list) != 0:
            invoice_row_list.append(html.Hr(className="text-muted mx-4 my-0"))

        # define components
        button = dbc.Button("Paid", size="sm", outline=True, color="primary", disabled=True)
        invoice_row_list.append(dbc.Row(children=[
            dbc.Col(children=[
                html.A(f"Invoice #{_id}", href="#", className=None),
                html.Div(f"Billed {_date}", className="small text-muted"),
            ], width="auto"),
            dbc.Col(button, width="auto"),
        ], align="center", justify="between", class_name="px-4 py-3"))

    # return result
    return dbc.Card(children=[
        dbc.CardHeader("Invoice History:", class_name="px-4 py-3"),
        html.Div(invoice_row_list, className=None),
    ], class_name=class_name)
