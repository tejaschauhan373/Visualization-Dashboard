from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import logging
import pandas as pd
from django.conf import settings

#marker=dict(color='rgb(0,0,0)' ,size=8)
#plot_bgcolor='rgba(100,0,100,0)'


class Plotly:

    def scatter(x_data,y_data,f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace1 = go.Scatter(df,
            x=x_data, y=y_data, mode='markers', name='points',
            marker=dict( size=8, opacity=0.4)
        )
        data = [trace1]
        layout = go.Layout(
            showlegend=True,
            autosize=True,
            #width=800,
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

    def Scatter(x_data, y_data , f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace = px.scatter(df, x=x_data, y=y_data, color='Country', height=500)
        plot_div = plot(trace, output_type='div', include_plotlyjs=True)
        return plot_div

    def bar(x_data, y_data , f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace = px.histogram(df, x=x_data, color=x_data, height=500)
        plot_div = plot(trace, output_type='div', include_plotlyjs=True)
        return plot_div

    def box(x_data,y_data,f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace = px.box(df,x=x_data, y=y_data,color=x_data, height=500)
        plot_div = plot(trace, output_type='div', include_plotlyjs=True)
        return plot_div

    def violin(x_data,y_data,f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace = px.violin(df,x=x_data, y=y_data,color=x_data, height=500)
        plot_div = plot(trace, output_type='div', include_plotlyjs=True)
        return plot_div

    def violin_box(x_data,y_data,f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace = px.violin(df,x=x_data, y=y_data,color=x_data,height=500,  box=True)
        plot_div = plot(trace, output_type='div', include_plotlyjs=True)
        return plot_div

    def violn_box_scatter (x_data,y_data,f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace = px.violin(df,x=x_data, y=y_data,color=x_data, height=500,box=True,points='all',animation_frame="Month Name")
        plot_div = plot(trace, output_type='div', include_plotlyjs=True)
        return plot_div

    def strip(x_data,y_data,f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.strip(df, x=x_data, y=y_data, color=x_data, animation_frame="Month Name", height=500)
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

