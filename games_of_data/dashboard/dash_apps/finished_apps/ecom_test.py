import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import traceback
from jupyter_dash import JupyterDash
from django_plotly_dash import DjangoDash
from urllib.request import urlopen
from django.conf import settings
import json
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash("vis", external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")

coulmn_names = ['country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap',
                'iso_alpha', 'iso_num', 'total_bill', 'tip', 'sex', 'smoker', 'day',
                'time', 'size', 'fips', 'unemp']
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

coulmn_name3d = coulmn_names + ['petal_width', 'sepal_width', 'sepal_length']
app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H5(children='Basic Plots'),
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column1',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    placeholder='select x-axis'
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column1',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    placeholder='select y-axis'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='color1',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    placeholder='select color column')
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='graph_type1',
                    options=[{'label': i, 'value': i} for i in ['Scatter', 'Line',
                                                                'Bar', 'Pie',
                                                                'Bubble']],
                    placeholder='select graph type'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

            # html.Div(children='''
            #     Dash: A web application framework for Python.
            # '''),

            dcc.Graph(
                id='graph1',
                figure=fig1
            ),
        ], className='six columns'),
        html.Div([
            html.H5(children='Statistical Plots'),
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column2',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    placeholder='select x-axis'
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column2',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    placeholder='select y-axis'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='color2',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    placeholder='select color column')
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='graph_type2',
                    options=[{'label': i, 'value': i} for i in ['Error Bars', 'Box Plots',
                                                                'Histograms', 'Displots',
                                                                '2D Histograms']],
                    placeholder='select graph type'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

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
            html.H5(children='Maps Plots'),
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column3',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    value='Fertility rate, total (births per woman)',
                    placeholder='select x-axis'
                )
            ],
                style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column3',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    placeholder='select y-axis'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='color3',
                    options=[{'label': i, 'value': i} for i in coulmn_names],
                    placeholder='select color column')
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='graph_type3',
                    options=[{'label': i, 'value': i} for i in ['Choropleth', 'Bubble']],
                    placeholder='select graph type'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
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
            html.H5(children='3D Plots'),
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column4',
                    options=[{'label': i, 'value': i} for i in coulmn_name3d],
                    placeholder='select x-axis'
                )
            ],
                style={'width': '48%', 'float': 'left', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column4',
                    options=[{'label': i, 'value': i} for i in coulmn_name3d],
                    placeholder='select y-axis'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='zaxis-column4',
                    options=[{'label': i, 'value': i} for i in coulmn_name3d],
                    placeholder='select z-axis'
                )
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='graph_type4',
                    options=[{'label': i, 'value': i} for i in ['Surface', 'Scatter']],
                    placeholder='select graph type'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            # html.Div([
            #     dcc.Dropdown(
            #         id='graph_type4',
            #         options=[{'label': i, 'value': i} for i in [1, 2, 3]],
            #         value='Life expectancy at birth, total (years)'
            #     )
            # ]),
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

file_path = os.path.join(settings.MEDIA_ROOT, "fips-unemp-16.csv")
df1 = px.data.gapminder()
df2 = px.data.tips()
df = pd.read_csv(file_path,
                 dtype={"fips": str})
df_concat = pd.concat([df1, df2, df], axis=1)
df = df_concat


@app.callback(
    Output('graph1', 'figure'),
    [Input('xaxis-column1', 'value'),
     Input('yaxis-column1', 'value'),
     Input('graph_type1', 'value'),
     Input('color1', 'value')],
)
def update_graph1(xaxis1, yaxis1, graph1, color1):
    try:
        fig1 = go.Figure()
        if graph1 is None:
            return fig1
        # df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")

        graph_type = graph1.lower()
        if graph_type == "bar":
            # graph_type = graph_type.lower()
            # if graph_type == "pie"
            fig1 = px.bar(df, y=yaxis1, x=xaxis1,hover_data=df.columns, color=color1)
            fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        elif graph_type == "pie":
            fig1 = px.pie(df, values=yaxis1, names=xaxis1, hover_data=df.columns)
        elif graph_type == "line":
            fig1 = px.line(df, y=yaxis1, x=xaxis1, hover_data=df.columns)
        elif graph_type == "scatter":
            fig1 = px.scatter(df, y=yaxis1, x=xaxis1, hover_data=df.columns)
        elif graph_type == "bubble":
            fig1 = px.scatter(df, y=yaxis1, x=xaxis1, hover_data=df.columns, color=color1)

        return fig1

    except:
        traceback.print_exc()


@app.callback(
    Output('graph2', 'figure'),
    [Input('xaxis-column2', 'value'),
     Input('yaxis-column2', 'value'),
     Input('graph_type2', 'value'),
     Input('color2', 'value')])
def update_graph2(xaxis2, yaxis2, graph2, color2):
    try:
        fig2 = go.Figure()
        if graph2 is None:
            return fig2
        # df = px.data.tips()
        # df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
        graph2 = graph2.lower()
        print(graph2)
        if graph2 == "box plots":
            fig2 = px.box(df, x=xaxis2, y=yaxis2, hover_data=df.columns, color=color2)
        elif graph2 == "histograms":
            fig2 = px.histogram(df, x=xaxis2, hover_data=df.columns, color=color2)
        elif graph2 == "displots":
            fig2 = px.histogram(df, x=xaxis2, y=yaxis2, hover_data=df.columns, color=color2)
        elif graph2 == 'error bars':
            fig2 = px.scatter(df, x=xaxis2, y=yaxis2, color=color2,
                              error_x=xaxis2, hover_data=df.columns, error_y=yaxis2)
        elif graph2 == "2d histograms":
            fig2 = px.density_heatmap(df, x=xaxis2, y=yaxis2)
        # elif graph_type == ""
        # print(fig2)
        return fig2
    except:
        traceback.print_exc()


@app.callback(
    Output('graph3', 'figure'),
    [Input('xaxis-column3', 'value'),
     Input('yaxis-column3', 'value'),
     Input('graph_type3', 'value'),
     Input('color3', 'value')])
def update_graph3(xaxis3, yaxis3, graph3, color3):
    try:
        fig3 = go.Figure()
        if graph3 is None:
            return fig3
        # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
        #                  dtype={"fips": str})
        graph3 = graph3.lower()
        print(graph3)
        if graph3 == "choropleth":
            fig3 = px.choropleth_mapbox(df, geojson=counties, locations=yaxis3, color=color3,
                                        range_color=(0, 12),
                                        color_continuous_scale="Viridis",
                                        mapbox_style="carto-positron",
                                        zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                                        opacity=0.5,
                                        hover_data=df.columns
                                        )
        elif graph3 == "bubbles":
            fig3 = px.scatter_geo(df, locations=xaxis3, color=color3,
                                  hover_name=df.columns,
                                  projection="natural earth")
        return fig3
    except:
        traceback.print_exc()


@app.callback(
    Output('graph4', 'figure'),
    [Input('xaxis-column4', 'value'),
     Input('yaxis-column4', 'value'),
     Input('zaxis-column4', 'value'),
     Input('graph_type4', 'value')])
def update_graph4(xaxis4, yaxis4, zaxis4, graph4):
    try:
        fig4 = go.Figure()
        if graph4 is None:
            return fig4
        graph4 = graph4.lower()
        print(graph4)
        if graph4 == "surface":
            fig4 = go.Figure(data=[go.Mesh3d(x=(70 * np.random.randn(N)),
                                             y=(55 * np.random.randn(N)),
                                             z=(40 * np.random.randn(N)),
                                             opacity=0.5,
                                             color='rgba(244,22,100,0.6)'
                                             )])
        elif graph4 == "scatter":
            # df = px.data.iris()
            fig4 = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                                 color='petal_length', symbol='species')
        return fig4
    except:
        traceback.print_exc()

#
# if __name__ == '__main__':
#     app.run_server(debug=True)
