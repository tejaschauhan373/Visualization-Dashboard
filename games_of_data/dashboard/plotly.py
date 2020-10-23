from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import logging
import pandas as pd
import numpy as np
from django.conf import settings
import plotly.offline as py
import plotly.tools as tls
import json
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as ctls
from chart_studio.grid_objs import Column, Grid
from plotly.subplots import make_subplots


# marker=dict(color='rgb(0,0,0)' ,size=8)
# plot_bgcolor='rgba(100,0,100,0)'


class Plotly:
    list = []
    def scatter(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace1 = go.Scatter(df,
                            x=x_data, y=y_data, mode='markers', name='points',
                            marker=dict(size=8, opacity=0.4)
                            )
        data = [trace1]
        layout = go.Layout(
            showlegend=True,
            autosize=True,
            # width=800,
            height=800,
            xaxis=dict(
                domain=[0, 0.85],
                showgrid=True,
                zeroline=False
            ),
            yaxis=dict(
                domain=[0, 0.85],
                showgrid=True,
                zeroline=False
            ),
            margin=dict(
                t=50
            ),
            hovermode='closest',
            bargap=0,
        )

        fig = go.Figure(data=data, layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def Scatter(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.scatter(df, x=x_data, y=y_data, color='Country', height=500)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def bar(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.histogram(df, x=x_data, color=x_data, height=500)
        fig.update_layout({'plot_bgcolor':'rgba(0, 0, 0, 0)'})
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def box(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.box(df, x=x_data, y=y_data, color=x_data, height=500)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def violin(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.violin(df, x=x_data, y=y_data, color=x_data, height=500)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def violin_box(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.violin(df, x=x_data, y=y_data, color=x_data, height=500, box=True)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="left"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def violn_box_scatter(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.violin(df, x=x_data, y=y_data, color=x_data, height=500, box=True, points='all',
                          animation_frame='Month Name')
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.3,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def strip(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.strip(df, x=x_data, y=y_data, color=x_data, animation_frame='Year', height=600)
        #fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.3,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def new(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.scatter(df, y=y_data, x=x_data)
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
               dict(
                   buttons=list(xbutton),
                   direction="down",
                   pad={"r": 10, "t": 10},
                   showactive=True,
                   x=0.1,
                   xanchor="left",
                   y=1.2,
                   yanchor="top"

               ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div
