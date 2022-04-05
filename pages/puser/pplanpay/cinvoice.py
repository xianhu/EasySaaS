# _*_ coding: utf-8 _*_

"""
Invoice History
"""

import dash_bootstrap_components as dbc
from dash import html

TAG = "user-billing-invoice"
INVOICE_LIST = [
    ("91240", "01/12/2020", 0),
    ("91230", "01/11/2020", 1),
    ("91220", "01/10/2020", 1),
    ("91210", "01/09/2020", 1),
]


def layout(class_name=None):
    """
    layout of component
    """
    # define components
    row_invoice_list = []
    for _id, _date, _flag in INVOICE_LIST:
        # define components
        if len(row_invoice_list) != 0:
            row_invoice_list.append(html.Hr(className="text-muted my-3"))

        # define components
        left = [
            html.A(f"Invoice #{_id}", href="#", className=None),
            html.Div(f"Billed {_date}", className="small text-muted"),
        ]
        right = dbc.Button("Paid", size="sm", outline=True, color="primary", disabled=True)

        # define components
        row_invoice_list.append(dbc.Row(children=[
            dbc.Col(left, width="auto", class_name=None),
            dbc.Col(right, width="auto", class_name=None),
        ], align="center", justify="between", class_name=None))

    # return result
    return dbc.Card(children=[
        dbc.CardHeader("Invoice History:", class_name="px-4 py-3"),
        html.Div(row_invoice_list, className="px-4 py-3"),
    ], class_name=class_name)
