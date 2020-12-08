# Python
import os
# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# this is like a template
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# change from here on
title = "Title"
# layout 
app.layout = html.Div(id="main-div", children=[
    html.Div(
        className="main-banner",
        children=[
            html.H2(
                className="h2-title",
                children=title
            ),
            html.Div(
                className="div-logo",
                children=html.Img(
                    className="logo", src=app.get_asset_url("logo.png")
                )
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)