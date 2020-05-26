import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.title = 'Fraction_MSA_map'
# path_to_file = 'test.csv'

path_to_file = 'MSA_overlapfraction_choro.csv'
df = pd.read_csv(path_to_file, dtype={"CountyFips": str})
available_MSAs = df['MSAName'].unique()
available_dates = df['date'].unique()
colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]
endpts = list(np.linspace(0, 1, len(colorscale) - 1))


fig1=px.choropleth(
            df,
            geojson=counties,
            locations='CountyFips',
            color='fraction_cases_t12',
            hover_data=['MSAName'],
            hover_name='CountyName',
            # hover_data=['MSAName', 'fraction_cases_t12'],
            scope="usa",
            color_continuous_scale= px.colors.sequential.Plasma,
            range_color=(0, 1),
            animation_frame='date',
            # title="The Fraction of Infections in the Second Half of a 2-Week Window",
            labels={'fraction_cases_t12':'fractions','MSAName':'MSA'}
            # animation_group="CountyFips"
)
fig1.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    autosize=False,
    width=1200,
    height=1000
    )


fig2=px.choropleth(
            df,
            geojson=counties,
            locations='CountyFips',
            color='fraction_deaths_t12',
            hover_data=['MSAName'],
            hover_name='CountyName',
            # hover_data=['MSAName', 'fraction_cases_t12'],
            scope="usa",
            color_continuous_scale= px.colors.sequential.Plasma,
            range_color=(0, 1),
            animation_frame='date',
            # title="The Fraction of Infections in the Second Half of a 2-Week Window",
            labels={'fraction_deaths_t12':'fractions','MSAName':'MSA'}
            # animation_group="CountyFips"
)
fig2.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    autosize=False,
    width=1200,
    height=1000
    )

app.layout = html.Div([
                html.Div(children='The Fraction of Infections in the Second Half of a 2-Week Window', style={
                        'textAlign': 'left',
                        'color': '#111111',
                        'font': 20
                }),
                html.Div([dcc.Graph(figure=fig1)], style={'width': '90%', 'display': 'inline-block'}),
                html.Div(children='The Fraction of Deaths in the Second Half of a 2-Week Window', style={
                        'textAlign': 'left',
                        'color': '#111111',
                        'font': 20
                }),
                html.Div([dcc.Graph(figure=fig2)], style={'width': '90%', 'display': 'inline-block'})
])



if __name__ == '__main__':
    app.run_server(debug=True)
#
