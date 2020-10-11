from django.shortcuts import render,HttpResponse
from plotly.offline import plot
import plotly.graph_objs as go
import openpyxl
import pandas as pd
import numpy as np
from django.conf import settings
from .models import Customer
from django.core.files.storage import FileSystemStorage
# Create your views here.

dataframe = pd.DataFrame()
def table_upload(request):
    if "GET" == request.method:
        return render(request, 'dashboard/tables.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        df = pd.read_excel(excel_file)
        csv_file = df.to_csv(settings.MEDIA_ROOT+'/'+(excel_file.name).replace('.xlsx','.csv'))
        # you may put validations here to check extension or file size
        request.session['file'] = (excel_file.name).replace('.xlsx','.csv')

        excel_data = list()
        excel_heading = list()
        path = str(settings.MEDIA_ROOT + '/' + request.session.get('file'))
        f = open(path, 'r')
        rows = []
        frow = list()
        i = 0;
        for row in f:
            if i == 0:
                row = row[1:].strip('\n').split(',')
                print(row)
                excel_heading = row
                i = 1
            else:
                row = row.strip('\n').split(',')
                print(row)
                excel_data.append(row[1:])
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

def show_table(request):
    path = str(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    f = open(path, 'r')
    rows = []
    frow = list()
    i = 0;
    for row in f:
        if i == 0:
            row = row[1:].strip('\n').split(',')
            print(row)
            frow=row
            i=1
        else:
            row = row.strip('\n').split(',')
            print(row)
            rows.append(row[1:])
    return render(request,'dashboard/show_table.html',context={'frow':frow,
                                                               'rows':rows})

def chartjs(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    categ_columns = list(dataframe.select_dtypes(exclude=np.number).columns)
    num_columns = list(dataframe.select_dtypes(include=np.number).columns)
    return render(request,'dashboard/chart.html',{'categ_columns':categ_columns,
                                                  'num_columns':num_columns})

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request, 'register.html')


def register(request):
    fname = request.POST.get('firstname')
    lname = request.POST.get('lastname')
    uname = request.POST.get('username')
    pwd = request.POST.get('password')
    cpassword = request.POST.get('cpassword')
    usr = Customer.objects.filter(username=uname)
    if len(usr) == 0 and  pwd == cpassword:
        newuser = Customer.objects.create(username=uname, password=pwd, first_name=fname, last_name=lname)
        newuser.save()
        nuser = Customer.objects.get(username=uname)
        print(nuser.user_id)
        return render(request,'basic.html',{})
    else:
        print("here")
        return render(request, 'register.html', {'error': 'This username already exists'})



def auth_user(request):
    user = Customer.objects.filter(username=request.POST.get('username')).first()
    if user is not None:
        if user.password == request.POST.get('password'):
            request.session['user'] = user.user_id
            request.session['fname'] = user.first_name
            request.session['lname'] = user.last_name
            return render(request,'basic.html',{})
        else:
            return HttpResponse('invalid password')
    else:
        return HttpResponse('invalid username or password')


def logout(request):
    try:
        del request.session['user']
        del request.session['fname']
        del request.session['lname']
        del request.session['file']
    except KeyError:
        pass
    return render(request,'basic.html')