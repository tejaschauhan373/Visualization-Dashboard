from django.shortcuts import render,HttpResponse
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import openpyxl
import pandas as pd
import numpy as np
from django.conf import settings
from .models import Customer
from .plotly import Plotly
from django.core.files.storage import FileSystemStorage
# Create your views here.



def home(request):
    return render(request, 'basic.html')


def table_upload(request):
    if "GET" == request.method:
        return render(request, 'dashboard/tables.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        if('.xlsx' in excel_file.name):
            df = pd.read_excel(excel_file)
            csv_file = df.to_csv(settings.MEDIA_ROOT+'/'+(excel_file.name).replace('.xlsx','.csv'))
            request.session['file'] = (excel_file.name).replace('.xlsx', '.csv')
        else:
            df = pd.read_excel(excel_file)
            csv_file = df.to_csv(settings.MEDIA_ROOT + '/' + excel_file.name)
            request.session['file'] = excel_file.name

        excel_data = list()
        excel_heading = list()
        path = str(settings.MEDIA_ROOT + '/' + request.session.get('file'))
        f = open(path, 'r')
        rows = []
        frow = list()
        i = 0
        for row in f:
            if i == 0:
                row = row[1:].strip('\n').split(',')
                excel_heading = row
                i = 1
            else:
                row = row.strip('\n').split(',')
                excel_data.append(row[1:])
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
    i = 0
    for row in f:
        if i == 0:
            row = row[1:].strip('\n').split(',')
            frow=row
            i=1
        else:
            row = row.strip('\n').split(',')
            rows.append(row[1:])
    return render(request,'dashboard/show_table.html',context={'frow':frow,
                                                               'rows':rows})




#graphs

def chartjs(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    columns = list(df.columns)
    return render(request,'dashboard/chart.html',context = {'columns':columns[1:]})

def chart(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    columns = list(df.columns)
    convert_dict = {request.POST.get('y'): int}

    df = df.astype(convert_dict)


    x = list(df[request.POST.get('x')])
    #print(x)
    print(request.POST.get('x'))
    print(request.POST.get('y'))
    y = list(df[request.POST.get('y')])
    return render(request,'dashboard/chart.html',context = {'columns':columns[1:],
                                                             'x':x[1:11],
                                                             'y':y[1:11]})

def plotly(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    columns = list(df.columns)
    return render(request,'dashboard/plotly.html',context = {'columns':columns[1:]})

def plotly_chart(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    columns = list(df.columns)
    plot_div = None
    x = request.POST.get('x')
    y = request.POST.get('y')
    f = request.session.get('file')
    graph = request.POST.get('graph')
    graph_list = []
    if graph == 'Scatter':
        plot_div = Plotly.Scatter(x,y,f)
    if graph == 'bar':
        plot_div = Plotly.bar(x, y, f)
    if graph == 'box':
        plot_div = Plotly.box(x, y, f)
    if graph == 'violin':
        plot_div = Plotly.violin(x, y, f)
    if graph == 'violin_box':
        plot_div = Plotly.violin_box(x, y, f)
    if graph == 'violin_box_scatter':
        plot_div = Plotly.violn_box_scatter(x, y, f)
    if graph == 'strip':
        plot_div = Plotly.strip(x, y, f)
    return render(request, 'dashboard/plotly.html', context={'plot_div':plot_div,
                                                             'columns':columns})



#user login logout

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