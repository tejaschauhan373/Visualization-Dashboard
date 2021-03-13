import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime

df = pd.read_csv(r"D:\Tejas\personal projects\gitlab private\e-commerce-monitoring-system\games_of_data\dashboard\dash_apps\finished_apps\Flipkart.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Redmi Note 8 Pro', 'value': 'Redmi Note 8 Pro'},
            {'label': 'Redmi Note 9 Pro', 'value': 'Redmi Note 9 Pro'},
            {'label': 'S1 Pro', 'value': 'S1 Pro'}
        ],
        value='Redmi Note 8 Pro'
    ),
    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})
    # html.Div(id='dd-output-container')
])




@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    second_df = df[df['model_name'] == value]
    second_df["utc_time_stamp"] = [datetime.fromutctimestamp(i) for i in second_df["utc_time_stamp"]]
    fig = px.line(second_df, x="utc_time_stamp", y="price", colour= "model_name")
    return fig
    return 'You have selected "{}"'.format(value)


if __name__ == "__main__":
    app.run_server(debug=True)
