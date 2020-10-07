from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
# Create your views here.


def finance(request):
    startdate = datetime.datetime(2006, 1, 1)
    enddate = datetime.datetime(2016, 1, 1)
    BAC = data.DataReader("BAC", "yahoo", startdate, enddate)
    C = data.DataReader("C", "yahoo", startdate, enddate)
    GS = data.DataReader("GS", "yahoo", startdate, enddate)
    JPM = data.DataReader("JPM", "yahoo", startdate, enddate)
    MS = data.DataReader("MS", "yahoo", startdate, enddate)
    WFC = data.DataReader("WFC", "yahoo", startdate, enddate)
    x_data = list(BAC['Open'])
    y_data = list(BAC['Close'])
    plot_div = plot([go.Scatter(x=x_data, y=y_data,
                             mode='lines', name='test',
                             opacity=0.8)],
                    output_type='div')
    return render(request, "monitoring/finance.html", context={'plot_div': plot_div})
