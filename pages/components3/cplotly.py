# _*_ coding: utf-8 _*_

"""
plotly components
"""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# define data
IRIS = px.data.iris()
TIPS = px.data.tips()
GDPM = px.data.gapminder()
GDPM_O = GDPM.query("continent=='Oceania'")
MEDA_LONG = px.data.medals_long()
MEDA_WIDE = px.data.medals_wide()

# figure of scatter ==================================================================================================================
fig_scatter_1 = px.scatter(IRIS, x="sepal_width", y="sepal_length", color="species", size="petal_length", hover_data=["petal_width"])

fig_scatter_2 = px.scatter(IRIS, x="sepal_width", y="sepal_length", color="species", symbol="species")

fig_scatter_3 = px.scatter(IRIS, x="sepal_width", y="sepal_length", color="petal_length")

# figure of scatter: Facetting
fig_scatter_4 = px.scatter(TIPS, x="total_bill", y="tip", color="smoker", facet_col="sex", facet_row="time")

# figure of line: ====================================================================================================================
fig_line_1 = px.line(GDPM_O, x="year", y="lifeExp", color="country", markers=True)

fig_line_2 = px.line(GDPM_O, x="year", y="lifeExp", color="country", symbol="country")

# figure of line: graph_objects
N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

fig_line_3 = go.Figure()
fig_line_3.add_trace(go.Scatter(x=random_x, y=random_y0, mode="markers", name="markers"))
fig_line_3.add_trace(go.Scatter(x=random_x, y=random_y1, mode="lines+markers", name="lines+markers"))
fig_line_3.add_trace(go.Scatter(x=random_x, y=random_y2, mode="lines", name="lines"))

# figure of bar: =====================================================================================================================
fig_bar_1 = px.bar(MEDA_LONG, x="nation", y="count", color="medal", title="Long-Form Input")

fig_bar_2 = px.bar(MEDA_WIDE, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")

fig_bar_3 = px.bar(GDPM_O, x="year", y="pop", hover_data=["lifeExp", "gdpPercap"], color="country", labels={"pop": "population of Canada"}, height=400)

fig_bar_4 = px.bar(MEDA_LONG, x="medal", y="count", color="nation", text="nation")

# figure of bar: Grouped Bar Chart
animals = ["giraffes", "orangutans", "monkeys"]
fig_bar_5 = go.Figure(data=[
    go.Bar(name="SF Zoo", x=animals, y=[20, 14, 23]),
    go.Bar(name="LA Zoo", x=animals, y=[12, 18, 29])
])
fig_bar_5.update_layout(barmode="group")

# figure of pie: =====================================================================================================================
fig_pie_1 = px.pie(TIPS, values="tip", names="day")

fig_pie_2 = px.pie(TIPS, values="tip", names="day", color_discrete_sequence=px.colors.sequential.RdBu)

# figure of pie: color
color_discrete_map = {
    "Thur": "lightcyan",
    "Fri": "cyan",
    "Sat": "royalblue",
    "Sun": "darkblue",
}
fig_pie_3 = px.pie(TIPS, values="tip", names="day", color="day", color_discrete_map=color_discrete_map)
