from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
import openpyxl
import pandas as pd
import numpy as np
from django.core.files.storage import FileSystemStorage
# Create your views here.

dataframe = pd.DataFrame()
def table_upload(request):
    if "GET" == request.method:
        return render(request, 'dashboard/tables.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        fs = FileSystemStorage()
        fs.save(excel_file.name,excel_file)
        # you may put validations here to check extension or file size
        df = pd.read_excel(excel_file)
        dataframe = df
        print(df.columns)
        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        excel_heading = list()
        # iterating over the rows and
        # getting value from each cell in row
        i=0
        for row in worksheet.iter_rows():
            if(i==0):
                h_data = list()
                for cell in row:
                    excel_heading.append(str(cell.value))
                i = i+1
            else:
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                    excel_data.append(row_data)


    # x_data = list(df["Country"])
    # y_data = list(df["Profit"])
    # plot_div = plot([go.Scatter(x=x_data, y=y_data,
    #                          mode='markers+text', name='test',
    #                          opacity=0.8)],
    #                 output_type='div')
    return render(request, "dashboard/tables.html", context={
                                                           "excel_data":excel_data,
                                                           "excel_heading":excel_heading})

def table(request):
    return render(request , 'dashboard/tables.html')

def chartjs(request):
    categ_columns = list(dataframe.select_dtypes(exclude=np.number).columns)
    num_columns = list(dataframe.select_dtypes(include=np.number).columns)
    print(categ_columns)
    return render(request,'dashboard/chart.html',{'categ_columns':categ_columns,
                                                  'num_columns':num_columns})