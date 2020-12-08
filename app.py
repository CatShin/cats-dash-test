# Python
import os
import re
import json
import requests
import pandas as pd
# Dash
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


# templates
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# add authentication
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world',
    'Cat': 'Woop!'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# change from here...
title = "GB Swimming 2018/19 Seasons Bests"

# import data and make graph
psb_df = pd.read_csv('https://sportsdatasolutionsacademy.s3.eu-west-2.amazonaws.com/data/TeamGB_PSBs_All.csv')
swim_wrs = requests.get('https://sportsdatasolutionsacademy.s3.eu-west-2.amazonaws.com/data/world_records_swimming.json')
swim_wrs = json.loads(swim_wrs.text)[0]

def time_to_seconds(result_string):
    try:
        return float(result_string)
    except:
        mins, secs = result_string.split(':')
        mins = int(mins) * 60
        secs = float(secs)
        return mins + secs

for index, row in psb_df.iterrows():
    wr = swim_wrs[row['gender']][row['event']]
    percent_of_wr = (float(time_to_seconds(wr)) / float(time_to_seconds(row['result']))) * 100.00
    psb_df.at[index, 'percent_of_wr'] = round(percent_of_wr, 2)

psb_df[['distance', 'style']] = psb_df['event'].str.split(' ', 1, expand=True)
psb_df['distance'] = psb_df['distance'].str[:-1].astype(int)
psb_df = psb_df.sort_values(by=['style', 'distance'])

fig1 = px.strip(psb_df, x="event", y="percent_of_wr", color="gender", hover_data={"event": True, "gender": True, "person": True, "result": True, "percent_of_wr": False})
fig1.update_xaxes(title_text="Event")
fig1.update_yaxes(title_text="Percent of World Record (%)")
fig1.update_layout(paper_bgcolor="white")
fig1.update_layout(height=600)

# layout
app.layout = html.Div(
    id="main-div",
    children=[
        html.Div(
            className="main-banner",
            children=[
                html.H2(className="h2-title", children=title),
                html.Div(
                    className="div-logo",
                    children=html.Img(
                        className="logo", src=app.get_asset_url("logo.png")
                    )
                )
            ]
        ),
        dcc.Graph(
            id='psb_swim_graph',
            figure=fig1
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)