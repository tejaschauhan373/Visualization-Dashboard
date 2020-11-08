from django.shortcuts import render, HttpResponse
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from django.conf import settings
from .models import Customer
from .plotly import Plotly
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# Create your views here.


# home page
def home(request):
    return render(request, 'basic.html')


# upload table
def table_upload(request):
    if "GET" == request.method:
        return render(request, 'dashboard/tables.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        if ('.xlsx' in excel_file.name):
            df = pd.read_excel(excel_file)
            csv_file = df.to_csv(settings.MEDIA_ROOT + '/' + (excel_file.name).replace('.xlsx', '.csv'))
            request.session['file'] = (excel_file.name).replace('.xlsx', '.csv')
        if('.csv' in excel_file.name):
            df = pd.read_csv(excel_file)
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
        "excel_data": excel_data,
        "excel_heading": excel_heading})


# show table
def table(request):
    return render(request, 'dashboard/tables.html')


def show_table(request):
    path = str(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    f = open(path, 'r')
    rows = []
    frow = list()
    i = 0
    for row in f:
        if i == 0:
            row = row[1:].strip('\n').split(',')
            frow = row
            i = 1
        else:
            row = row.strip('\n').split(',')
            rows.append(row[1:])
    return render(request, 'dashboard/show_table.html', context={'frow': frow,
                                                                 'rows': rows})


# graphs

def chartjs(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    columns = list(df.columns)
    return render(request, 'dashboard/chart.html', context={'columns': columns[1:]})


def chart(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    columns = list(df.columns)
    convert_dict = {request.POST.get('y'): int}

    df = df.astype(convert_dict)

    x = list(df[request.POST.get('x')])
    # print(x)
    print(request.POST.get('x'))
    print(request.POST.get('y'))
    y = list(df[request.POST.get('y')])
    return render(request, 'dashboard/chart.html', context={'columns': columns[1:],
                                                            'x': x[1:11],
                                                            'y': y[1:11]})


# plotly page
def plotly(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    columns = list(df.columns)
    return render(request, 'dashboard/plotly.html', context={'columns': columns[1:]})


# plotly graph

def plotly_chart(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '/' + request.session.get('file'))
    tab = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    tab.update_layout(template="plotly_white")
    plot_div = None
    x = request.POST.get('x')
    y = request.POST.get('y')
    f = request.session.get('file')
    graph = request.POST.get('graph')
    graph_list = []
    if graph == 'Scatter':
        plot_div = Plotly.Scatter(x, y, f)
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
    table = plot(tab, output_type='div', include_plotlyjs=True)
    return render(request, 'dashboard/plotly.html', context={'plot_div': plot_div,
                                                             'table':table})



def covid(request):
    return render(request,'dashboard/covid.html')
# user login logout

def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'register.html')


def register(request):
    fname = request.POST.get('firstname')
    lname = request.POST.get('lastname')
    uname = request.POST.get('username')
    pwd = request.POST.get('password')
    email = request.POST.get('email')
    cpassword = request.POST.get('cpassword')
    usr = Customer.objects.filter(username=uname)
    if len(usr) == 0 and pwd == cpassword:
        newuser = Customer.objects.create(username=uname, password=pwd, first_name=fname, last_name=lname, email=email)
        newuser.save()
        nuser = Customer.objects.get(username=uname)
        print(nuser.user_id)
        return render(request, 'basic.html', {})
    else:
        print("here")
        return render(request, 'register.html', {'error': 'This username already exists'})


# authenticate user

def auth_user(request):
    user = Customer.objects.filter(username=request.POST.get('username')).first()
    if user is not None:
        if user.password == request.POST.get('password'):
            request.session['user'] = user.user_id
            request.session['fname'] = user.first_name
            request.session['lname'] = user.last_name
            return render(request, 'basic.html', {})
        else:
            return render(request, 'login.html', {'message': "invalid password"})
    else:
        return render(request, 'login.html', {'message': "invalid username or password"})


# forgot password page
def reset(request):
    return render(request, 'email.html')


def resetpasswrodform(request):
    return render(request, 'resetpassword.html', {})


# forgot page email post request
def resetpassword(request):
    email = request.POST.get('email')
    usr = Customer.objects.filter(email=email)
    if (len(usr) != 0):
        sender_email = "akashdesai326@gmail.com"
        receiver_email = usr[0].email
        password = '@2020*qaZ'
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Visualize"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               Reset your password from below link<br>
               <hr>
               <a href="http://127.0.0.1:8000/dashboard/reset/password/form/">Reset your Password</a> you wanted.
            </p>
          </body>
        </html>
        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, msg.as_string()
            )

        return render(request, 'login.html')
    return render(request, 'password.html', {'message': "email id does not exists."})


# reset password page post request
def password(request):
    email = request.POST.get('email')
    pwd = request.POST.get('password')
    cpwd = request.POST.get('cpassword')
    usr = Customer.objects.filter(email=email)
    if (len(usr) != 0):
        if (pwd == cpwd):
            Customer.objects.filter(email=email).update(password=pwd)
            return render(request, 'login.html')
        return render(request, 'resetpassword.html', {"error": "your password does not match with confirm password."})
    return render(request, 'resetpassword.html', {"error": "Email id does not exists."})


# logout
def logout(request):
    try:
        del request.session['user']
        del request.session['fname']
        del request.session['lname']
        del request.session['file']
    except KeyError:
        pass
    return render(request, 'basic.html')
