# import dash_table
# import pandas as pd
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# from django_plotly_dash import DjangoDash
# from django.conf import settings

# app = DjangoDash("table")w
# df = pd.read_csv(settings.MEDIA_ROOT + '/' + 'data.csv')
# app.layout = dash_table.DataTable(
#     data=df.to_dict('records'),
#     columns=[{'id': c, 'name': c} for c in df.columns],
#     page_action='none',
#     style_table={'height': '300px', 'overflowY': 'auto'}
# )


#import pandas asw