from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import logging

class Plotly:
    def scatter(x_data,y_data):
        plot_div = plot([go.Scatter(x=x_data, y=y_data,
                                mode='markers+text', name='test',
                                opacity=0.8)],
                                output_type='div')
        return plot_div

    def bubble(x_data,y_data):
        plot_div = plot([go.Histogram(x=x_data,
                                    name='test',
                                    opacity=0.8)])
        return plot_div