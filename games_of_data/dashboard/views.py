from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
import openpyxl
# Create your views here.


def home(request):
    if "GET" == request.method:
        return render(request, 'dashboard/dash.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

    x_data = [0, 1, 2, 3]
    y_data = [x ** 2 for x in x_data]
    plot_div = plot([go.Scatter(x=x_data, y=y_data,
                             mode='lines', name='test',
                             opacity=0.8)],
                    output_type='div')
    return render(request, "dashboard/dash.html", context={'plot_div': plot_div,
                                                           "excel_data":excel_data})
