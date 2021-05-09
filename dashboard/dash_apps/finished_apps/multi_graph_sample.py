import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
fig1 = px.bar(df, y='pop', x='country', text='pop')
fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
df = px.data.iris()  # iris is a pandas DataFrame
fig2 = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                 size='petal_length', hover_data=['petal_width'])

import numpy as np

np.random.seed(1)

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

fig3 = go.Figure()

# Add traces
fig3.add_trace(go.Scatter(x=random_x, y=random_y0,
                          mode='markers',
                          name='markers'))
fig3.add_trace(go.Scatter(x=random_x, y=random_y1,
                          mode='lines+markers',
                          name='lines+markers'))
fig3.add_trace(go.Scatter(x=random_x, y=random_y2,
                          mode='lines',
                          name='lines'))

df = px.data.iris()
fig4 = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                    color='petal_length', symbol='species')
# fig4.show()

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column1',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Fertility rate, total (births per woman)'
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column1',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Life expectancy at birth, total (years)'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='graph_type1',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Life expectancy at birth, total (years)'
                )
            ]),
            # html.H3(children='Hello Dash'),

            # html.Div(children='''
            #     Dash: A web application framework for Python.
            # '''),

            dcc.Graph(
                id='graph1',
                figure=fig1
            ),
        ], className='six columns'),
        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='xaxis-column2',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Fertility rate, total (births per woman)'
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column2',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Life expectancy at birth, total (years)'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='graph_type2',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Life expectancy at birth, total (years)'
                )
            ]),

            # html.H3(children='Hello Dash'),

            # html.Div(children='''
            #     Dash: A web application framework for Python.
            # '''),

            dcc.Graph(
                id='graph2',
                figure=fig2
            ),
        ], className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column3',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Fertility rate, total (births per woman)'
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column3',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Life expectancy at birth, total (years)'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='graph_type3',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Life expectancy at birth, total (years)'
                )
            ]),
            # html.H3(children='Hello Dash'),

            #     html.Div(children='''
            #     Dash: A web application framework for Python.
            # '''),

            dcc.Graph(
                id='graph3',
                figure=fig3
            ),
        ], className='six columns'),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column4',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Fertility rate, total (births per woman)'
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column4',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Life expectancy at birth, total (years)'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='graph_type4',
                    options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                    value='Life expectancy at birth, total (years)'
                )
            ]),
            # html.H3(children='Hello Dash'),

            #  html.Div(children='''
            #     Dash: A web application framework for Python.
            # '''),

            dcc.Graph(
                id='graph4',
                figure=fig4,

            ),
        ], className='six columns'),
    ], className='row'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
