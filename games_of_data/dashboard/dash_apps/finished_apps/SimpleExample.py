# # import dash
# # import dash_core_components as dcc
# # import dash_html_components as html
# #
# from django_plotly_dash import DjangoDash
# #
# # app = DjangoDash('SimpleExample')  # replaces dash.Dash
# #
# # app.layout = html.Div([
# #     dcc.RadioItems(
# #         id='dropdown-color',
# #         options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
# #         value='red'
# #     ),
# #     html.Div(id='output-color'),
# #     dcc.RadioItems(
# #         id='dropdown-size',
# #         options=[{'label': i,
# #                   'value': j} for i, j in [('L', 'large'), ('M', 'medium'), ('S', 'small')]],
# #         value='medium'
# #     ),
# # ])
# #
# #
# # @app.callback(
# #     dash.dependencies.Output('output-size', 'children'),
# #     [dash.dependencies.Input('dropdown-color', 'value'),
# #      dash.dependencies.Input('dropdown-size', 'value')])
# # def callback_size(dropdown_color, dropdown_size):
# #     return "The chosen T-shirt is a %s %s one." % (dropdown_size,
# #                                                    dropdown_color)
#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.express as px
#
# import pandas as pd
#
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
#
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = dash.Dash('SimpleExample', external_stylesheets=external_stylesheets)
#
# # app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)
#
# app.layout = html.Div([
#     dcc.Graph(id='graph-with-slider'),
#     dcc.Slider(
#         id='year-slider',
#         min=df['year'].min(),
#         max=df['year'].max(),
#         value=df['year'].min(),
#         marks={str(year): str(year) for year in df['year'].unique()},
#         step=None
#     )
# ])
#

# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     [Input('year-slider', 'value')])
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#
#     fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                      size="pop", color="continent", hover_name="country",
#                      log_x=True, size_max=50)
#
#     fig.update_layout(transition_duration=500)
#
#     return fig
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
