from django.shortcuts import render
from .helper import filter_by_ram
from .database import execute_aggregation
from collections import defaultdict
from plotly.offline import plot
import plotly.graph_objs as go


# Create your views here.
from .plotly import grouped_bar


def home(request):
    return render(request, "monitoring/retailers.html")


def avg_price_by_ram(request):
    agr = [{'$group': {'_id': {"company": '$company', "ram": "$ram"}, "sum": {"$sum": "$price"}, "count": {"$sum": 1}}}]
    list_of_items = execute_aggregation("mobile", agr).limit(10)
    res = defaultdict(list)
    list_of_items = filter_by_ram(list_of_items)
    for val in list_of_items:
        res[val["company"]].append({"RAM": val["RAM"], "Avg_price": val["Avg_price"]})

    graph_div = []

    # for key, company_data in res.items():
    #     company_data = sorted(company_data, key=lambda x: x["RAM"])
    #     all_ram = [data["RAM"] for data in company_data]
    #     avg_price = [data["Avg_price"] for data in company_data]
    #     graph_div.append(plot([go.Bar(x=avg_price,
    #                                   y=all_ram, name=key, opacity=0.8)]))
    return render(request, "monitoring/finance.html", context={'plot_div': grouped_bar(res)})
