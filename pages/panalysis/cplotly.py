# _*_ coding: utf-8 _*_

"""
plotly components
"""

import plotly.express as px

DATA = px.data.iris()

# basic scatter
fig_scatter = px.scatter(
    DATA, x="sepal_width", y="sepal_length",
    color="species", size="petal_length", hover_data=["petal_width"],
)
