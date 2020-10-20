from django.shortcuts import render
from .helper import filter_by_ram
from .database import execute_aggregation
from collections import defaultdict
from plotly.offline import plot
import plotly.graph_objs as go


def grouped_bar(res):
    RAM = ["2 GB", "4 GB", "6 GB", "8 GB"]
    data = []
    for key, company_data in res.items():
        company_data = sorted(company_data, key=lambda x: x["RAM"])
        avg_price = [data["Avg_price"] for data in company_data]
        data.append(go.Bar(name=key, x=RAM, y=avg_price))
    fig = go.Figure(data=data)
    fig.update_layout(barmode='group')
    fig.show()
    plot_div = plot(fig, output_type='div', include_plotlyjs=True)
    return plot_div
