# _*_ coding: utf-8 _*_

"""
plotly basic page
"""

import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html

DATA = px.data.iris()


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    figure = px.scatter(
        DATA, x="sepal_width", y="sepal_length",
        color="species", size="petal_length", hover_data=["petal_width"],
    )

    # return result
    return dbc.Card(children=[
        dbc.CardHeader("Plotly Basic Page", class_name="px-4 py-3"),
        html.Div(dcc.Graph(figure=figure), className="p-0"),
    ], class_name=None, style={"minHeight": "600px"})
