from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
# Create your views here.


def home(request):
    x_data = [0, 1, 2, 3]
    y_data = [x ** 2 for x in x_data]
    plot_div = plot([go.Scatter(x=x_data, y=y_data,
                             mode='lines', name='test',
                             opacity=0.8)],
                    output_type='div')
    return render(request, "dashboard/dash.html", context={'plot_div': plot_div})
