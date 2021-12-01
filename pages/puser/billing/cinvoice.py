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


def layout(pathname, search):
    """
    layout of card
    """
    # define components
    invoice_row_list = [html.Div("Invoice History:", className="border-bottom p-4")]
    for _id, _date, _flag in INVOICE_LIST:
        if len(invoice_row_list) != 1:
            invoice_row_list.append(html.Hr(className="text-muted mx-4 my-0"))

        if _flag == 0:
            button = dbc.Button("Pay Now", size="sm", outline=True, color="primary")
        else:
            button = dbc.Button("Paid", size="sm", outline=True, color="primary", disabled=True)
        invoice_row_list.append(dbc.Row(children=[
            dbc.Col(children=[
                html.A(f"Invoice #{_id}", href="#"),
                html.Div(f"Billed {_date}", className="small text-muted"),
            ], width="auto"),
            dbc.Col(button, width="auto"),
        ], align="center", justify="between", class_name="p-4"))

    # return result
    return dbc.Card(children=invoice_row_list, class_name="mb-4")
