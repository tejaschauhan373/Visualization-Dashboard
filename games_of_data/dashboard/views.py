import os
import time
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import urllib.parse
import smtplib, ssl
import traceback
import mimetypes
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, redirect
from plotly.offline import plot
from django.conf import settings
from .models import Customer, SignUpVerification, File
from .plotly import Plotly
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
from .mail_sending import send_mail
from uuid import uuid1
from service.azure_service import upload_file_to_azure, delete_file_from_azure, get_file_from_azure, get_downloadable_url_of_azure_file
# Create your views here.


# home page
from games_of_data.settings import MEDIA_ROOT


def home(request):
    return render(request, 'basic.html')


# Delete saved file of user
def file_delete(request, azure_file_name: str):
    if "user" not in request.session:
        return render(request, 'basic.html')
    File.objects.filter(azur_file_name = azure_file_name).delete()
    DIR_DESTINATION = os.path.join(MEDIA_ROOT, str(request.session['user']))
    file_path = os.path.join(DIR_DESTINATION, azure_file_name)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            traceback.print_exc()
        try:
            delete_file_from_azure(request.session['user'], azure_file_name)
        except:
            traceback.print_exc()
    return redirect(get_profile_picture)

# Display saved file of user
def view_user_file(request, azure_file_name: str):
    if "user" not in request.session:
        return render(request, 'basic.html')
    file_details = File.objects.filter(azur_file_name = azure_file_name).first()    
    if file_details:
        DIR_DESTINATION = os.path.join(MEDIA_ROOT, str(request.session['user']))
        file_path = os.path.join(DIR_DESTINATION, azure_file_name)
        if not os.path.exists(file_path):
            if not os.path.exists(DIR_DESTINATION):
                os.makedirs(DIR_DESTINATION)
            get_file_from_azure(str(request.session['user']), azure_file_name, file_path)
        print(file_path)
        f = open(file_path, 'r')
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
        f.close()
        return render(request, 'dashboard/show_table.html', context={'frow': frow,
                                                                    'rows': rows})
    else:
        return render(request, 'basic.html', {'user_id': request.session['user']})


# Download user's saved file
def download_file(request, azure_file_name: str):
    if "user" not in request.session:
        return render(request, 'basic.html')
    file_details = File.objects.filter(azur_file_name = azure_file_name).first()
    if file_details is None:
        return HttpResponse(f"You may have deleted {file_details.file_name} file")
    DIR_DESTINATION = os.path.join(MEDIA_ROOT, str(request.session['user']))
    downloads_directory = os.path.join(DIR_DESTINATION,"downloads")
    if not os.path.exists(DIR_DESTINATION):
        os.makedirs(DIR_DESTINATION)
        os.makedirs(downloads_directory)
    elif not os.path.exists(downloads_directory):
        os.makedirs(downloads_directory)
    downloadable_file_path = os.path.join(downloads_directory, f"{uuid1().hex}"+azure_file_name)
    get_file_from_azure(str(request.session['user']), azure_file_name, downloadable_file_path)
    with open(downloadable_file_path, 'r') as file:
        mime_type, _ = mimetypes.guess_type(downloadable_file_path)
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = f"attachment; filename={file_details.file_name}"
    os.remove(downloadable_file_path)
    return response


# get profile picture page
def get_profile_picture(request):
    if "user" not in request.session:
        return render(request, 'basic.html')
    is_files = "false"
    is_images = "false"
    user_id = request.session["user"]
    user = Customer.objects.filter(user_id=user_id).first()
    list_of_images = File.objects.filter(user_id=user_id, file_type="img")
    list_of_files = File.objects.filter(user_id=user_id, file_type="csv")
    list_of_files = [[file.file_name, file.azur_file_name] for file in list_of_files]
    list_of_images = [[file.file_name, file.azur_file_name] for file in list_of_images]
    if len(list_of_files) > 0:
        is_files = "true"
    if len(list_of_images) > 0:
        is_images = "true"

    return render(request, 'profile.html',
                  {'user_fname': user.first_name, 'user_lname': user.last_name, 'username': user.username,
                   "images": list_of_images, "files": list_of_files, "is_images": is_images, "is_files": is_files})


# upload new profile photo
def upload_new_profile_picture(request, user_id):
    # TODO: save new profile picture of user
    pass


# remove profile picture of user
def remove_profile_picture(request, user_id):
    # TODO: remove profile picture of user
    pass

# upload table
def table_upload(request):
    if "user" not in request.session:
        return render(request, 'basic.html')
    if "GET" == request.method:
        return render(request, 'dashboard/tables.html', {})
    else:
        save_to_cloud_checkbox = list(request.POST.getlist('checks[]'))
        
    excel_file = request.FILES["excel_file"]
    if ('.xlsx' in excel_file.name):
        df = pd.read_excel(excel_file)
        csv_file = df.to_csv(settings.MEDIA_ROOT + '/' + (excel_file.name).replace('.xlsx', '.csv'))
        request.session['file'] = (excel_file.name).replace('.xlsx', '.csv')
    elif ('.csv' in excel_file.name):
        df = pd.read_csv(excel_file)
        csv_file = df.to_csv(settings.MEDIA_ROOT + '/' + excel_file.name)
        request.session['file'] = excel_file.name
    else:
        return HttpResponse("Please enter excel or csv files only")
    DIR_DESTINATION = os.path.join(MEDIA_ROOT, str(request.session['user']))
    if not os.path.exists(DIR_DESTINATION):
        os.mkdir(DIR_DESTINATION)
    azure_file_name = uuid1().hex+f".{excel_file.name.split('.')[-1]}"
    request.session["file_name_dict"] = {"user_file_name": excel_file.name, "azure_file_name": azure_file_name}
    fs = FileSystemStorage(location=DIR_DESTINATION)
    file_path = os.path.join(DIR_DESTINATION, azure_file_name)
    print(azure_file_name, DIR_DESTINATION)
    print(excel_file)
    fs.save(azure_file_name, excel_file)
    if len(save_to_cloud_checkbox) > 0:
        File.objects.create(user_id=Customer.objects.filter(user_id=request.session["user"])[0], file_name=excel_file.name,
                            azur_file_name=azure_file_name,
                            azur_file_share="test", azur_container=str(request.session["user"]), file_type="csv",
                            file_size=fs.size(azure_file_name))
        if excel_file.name.split('.')[-1] == "csv":  
            content_type = "text/csv"
        else:
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"             
        upload_file_to_azure(directory_name=request.session["user"], azure_file_name= azure_file_name, local_file_path=file_path,content_type=content_type)
    excel_data = list()
    excel_heading = list()
    f = open(file_path, 'r')
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
    f.close()
    return render(request, "dashboard/tables.html", context={
        "excel_data": excel_data,
        "excel_heading": excel_heading})


# show table
def table(request):
    return render(request, 'dashboard/tables.html')


def show_table(request):
    if "user" not in request.session:
        return render(request, 'basic.html')
    DIR_DESTINATION = os.path.join(MEDIA_ROOT, str(request.session['user']))
    azure_file_name = request.session['file_name_dict']['azure_file_name']
    file_path = os.path.join(DIR_DESTINATION, azure_file_name)
    print(file_path)
    f = open(file_path, 'r')
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
    f.close()
    return render(request, 'dashboard/show_table.html', context={'frow': frow,
                                                                 'rows': rows})


# graphs

# plotly page
def plotly(request):
    if "user" not in request.session:
        return render(request, 'basic.html')
    excel_data = list()
    excel_heading = list()
    DIR_DESTINATION = os.path.join(MEDIA_ROOT, str(request.session['user']))
    file_path = os.path.join(DIR_DESTINATION,  request.session['file_name_dict']['azure_file_name'])
    if not os.path.exists(file_path):
        return render(request, 'basic.html', {'user_id': request.session['user']})
    else:
        f = open(file_path, 'r')
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
        f.close()
        return render(request, 'dashboard/plotly.html', context={"excel_data": excel_data,
                                                                "excel_heading": excel_heading})


# plotly graph

def plotly_chart(request):
    if "user" not in request.session:
        return render(request, 'basic.html')
    DIR_DESTINATION = os.path.join(MEDIA_ROOT, str(request.session['user']))
    file_path = os.path.join(DIR_DESTINATION,  request.session['file_name_dict']['azure_file_name'])
    if not os.path.exists(file_path):
        return render(request, 'basic.html', {'user_id': request.session['user']})
    df = pd.read_csv(file_path)
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
    color = request.POST.get('color')
    graph = request.POST.get('graph')
    graph_list = []
    if graph == 'Scatter':
        plot_div = Plotly.Scatter(x, y, f, color)
    if graph == 'line':
        plot_div = Plotly.line(x, y, f, color)
    if graph == 'bar':
        plot_div = Plotly.bar(x, y, f, color)
    if graph == 'pie':
        plot_div = Plotly.pie(x, y, f, color)
    if graph == 'bubble':
        plot_div = Plotly.bubble(x, y, f, color)
    if graph == 'gantt':
        plot_div = Plotly.gantt(x, y, f, color)
    if graph == 'box':
        plot_div = Plotly.box(x, y, f, color)
    if graph == 'boxscatter':
        plot_div = Plotly.box_scatter(x, y, f, color)
    if graph == 'violin':
        plot_div = Plotly.violin(x, y, f, color)
    if graph == 'violin_box':
        plot_div = Plotly.violin_box(x, y, f, color)
    if graph == 'violin_box_scatter':
        plot_div = Plotly.violn_box_scatter(x, y, f, color)
    if graph == 'strip':
        plot_div = Plotly.strip(x, y, f, color)
    # table = plot(tab, output_type='div', include_plotlyjs=True)
    excel_data = list()
    excel_heading = list()
    DIR_DESTINATION = os.path.join(MEDIA_ROOT, str(request.session['user']))
    file_path = os.path.join(DIR_DESTINATION,  request.session['file_name_dict']['azure_file_name'])
    f = open(file_path, 'r')
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
    f.close()
    return render(request, 'dashboard/plotly.html', context={'plot_div': plot_div,
                                                             # 'table':table,
                                                             "excel_data": excel_data,
                                                             "excel_heading": excel_heading
                                                             })

def covid(request):
    return render(request, 'dashboard/covid.html')


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
    time_stamp = time.time()
    send_mail(email, "Verification mail", uname, time_stamp)
    usr = Customer.objects.filter(username=uname)
    if len(usr) == 0 and pwd == cpassword:
        newuser = SignUpVerification.objects.create(username=uname, password=pwd, first_name=fname, last_name=lname,
                                                    email=email, signup_timestamp=time_stamp)
        newuser.save()
        return render(request, 'alert-message.html', {"message_type": "info",
                                                      "message": "Mail has been sent to your email address, please verify it."})
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
            return render(request, 'basic.html', {'user_id': user.user_id})
        else:
            return render(request, 'login.html', {'message': "invalid password"})
    else:
        return render(request, 'login.html', {'message': "invalid username or password"})


# forgot password page
def reset(request):
    return render(request, 'email.html')


def confirmation(request, time_stamp):
    time_stamp = float(time_stamp)
    user = SignUpVerification.objects.filter(signup_timestamp=time_stamp).first()
    if user is None or user.signup_timestamp != float(time_stamp):
        return render(request, 'alert-message.html',
                      {"message_type": "fail", "message": "Can't Verified, Please try again"})
    elif user.signup_timestamp == float(time_stamp):
        SignUpVerification.objects.filter(signup_timestamp=time_stamp).delete()
        newuser = Customer.objects.create(username=user.username, password=user.password, first_name=user.first_name,
                                          last_name=user.last_name, email=user.email)
        newuser.save()
        return render(request, 'alert-message.html', {"message_type": "success", "message": "Verified Successfully"})


def resetpasswrodform(request):
    time_stamp = request.GET.get('stamp')
    user_id = request.GET.get('id')
    user = Customer.objects.filter(user_id=user_id).first()
    link_create_date = datetime.fromtimestamp(float(time_stamp))
    current_date = datetime.now()
    difference = current_date - link_create_date
    if difference.seconds > 300 or user is None or user.forgot_pwd_timestamp != float(time_stamp):
        return HttpResponse("URL is expired")
    else:
        return render(request, 'resetpassword.html', {"user_id": int(user_id)})


def send_change_password_page(request):
    return render(request,'reset-password.html')

def change_password_after_login(request):
    if "user" not in request.session:
        return render(request, 'basic.html')
        
    user_id = request.session['user']
    user = Customer.objects.filter(user_id=user_id).first()
    new_password_first = request.POST.get('new_password_first')
    new_password_second = request.POST.get('new_password_second')
    current_password = request.POST.get('current_password')
    
    print(new_password_second, new_password_first)
    if new_password_first != new_password_second:
        return render(request, 'reset-password.html', {'message': "new password and confirm password are different!", "success":"false"})
    
    if user.password == current_password:
        Customer.objects.filter(user_id=user_id).update(password=new_password_second)
        return render(request, 'reset-password.html', {'message': "Password changed successfully!", "success":"true"})
    else:
        return render(request, 'reset-password.html', {'message': "invalid password", "success":"false"})
    
# forgot page email post request
def resetpassword(request):
    email = request.POST.get('email')
    usr = Customer.objects.filter(email=email)
    if (len(usr) != 0):
        sender_email = "dream13tejas@gmail.com"
        receiver_email = usr[0].email
        strg = usr[0].user_id
        password = 'RANVEER@2018'
        msg = MIMEMultipart('alternative')

        msg['Subject'] = "Visualize"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        time_stamp = time.time()
        params = {'id': f"{strg}", 'stamp': f'{time_stamp}'}
        Customer.objects.filter(user_id=strg).update(forgot_pwd_timestamp=time_stamp)
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               Reset your password from below link<br>
               <hr>
               <a href="http://127.0.0.1:8000/dashboard/reset/password/form/""" + f"?{urllib.parse.urlencode(params)}" + """">Reset your Password</a> you wanted.
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

        return render(request, 'alert-message.html', {"message_type": "info",
                                                      "message": "Reset password link has been sent to your email address!"})
    return render(request, 'password.html', {'message': "email id does not exists."})


# reset password page post request
def password(request, user_id):
    id = user_id
    pwd = request.POST.get("password")
    cpwd = request.POST.get('cpassword')
    usr = Customer.objects.filter(user_id=user_id)
    if (len(usr) != 0):
        if (pwd == cpwd):
            Customer.objects.filter(user_id=user_id).update(password=pwd)
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
