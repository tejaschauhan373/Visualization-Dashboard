import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from jupyter_dash import JupyterDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df_bar, x="Fruit", y="Amount", color="City", barmode="group", height=300, width=800)

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='demo-dropdown',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='NYC'
                )
            ], style={"width": "50%"},),
            html.H3(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='graph1',
                figure=fig
            ),
        ], className='six columns'),
        html.Div([
            html.H3(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='graph2',
                figure=fig
            ),
        ], className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.Div([
            html.H3(children='Hello Dash'),

            html.Div(children='''
            Dash: A web application framework for Python.
        '''),

            dcc.Graph(
                id='graph3',
                figure=fig
            ),
        ], className='six columns'),
        html.Div([
            html.H3(children='Hello Dash'),

            html.Div(children='''
               Dash: A web application framework for Python.
           '''),

            dcc.Graph(
                id='graph4',
                figure=fig,

            ),
        ], className='six columns'),
    ], className='row'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
