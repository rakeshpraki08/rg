import asyncio
from datetime import datetime
from multiprocessing import context
from urllib import response
from django.shortcuts import get_object_or_404, render, redirect
from django.db import connection
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
import psycopg2
import pandas as pd
import os
import cx_Oracle, json
import time, math, ast

from .models import CustomUser, Regions, Reports, Reports_Data
from .forms import ReportsForm, RegionsForm, CustomUserCreationForm, CustomUserChangeForm, CustomRegisterCreationForm

from django.contrib.auth.models import User
from django.db.models import Q

# from .tasks import extract_func

from django.contrib.auth.decorators import login_required

# from .thread import ReportExtractThread


# Create your views here.
# ---------------------------



from django.contrib import messages


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

# --------------------------------------------------
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
# from .threads import EmailThread
from django.urls import reverse
# from validate_email import validate_email
# ----------------------------------------------------


import threading
# from django.core.mail import EmailMessage

from .tasks import *

#global declaration, inlude the list variable in all the views in context

list = Regions.objects.all()

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        try:
            print("inside thread")
            self.email.send()
        except Exception as e:
            print("thread error ", e)



# --------------- e-mail verification ----------
def send_activation_email(user, request):
    print("inside send_activation")
    # print(user)
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('query_app/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    print("after email body in send_activation")

    email = EmailMessage(subject=email_subject, 
                         body=email_body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[user.email]
                         )
    
    EmailThread(email).start()
    # if not settings.TESTING:
    #     EmailThread(email).start()
        
        
def activate_user(request, uidb64, token):
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = CustomUser.objects.get(pk=uid)

    except Exception as e:
        print("activate_user error",e)
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('query_app:login-page'))

    return render(request, 'query_app/activate-failed.html', {"user": user})



@unauthenticated_user
def registerPage(request):
    form = CustomRegisterCreationForm()
    
    if request.method == 'POST':
        form = CustomRegisterCreationForm(request.POST)
        print('form data in register ', form)
        if form.is_valid():
            form.save()
            form.save_m2m()
            user = form.cleaned_data.get('email')
            print("post register", user)
            # messages.success(request, 'Account created for ' + user)
            
            # user2 = CustomUser.objects.get(mail=user)
            # user2 = CustomUser.objects.CustomRegisterCreationForm(username=username, email=email)
            # print("checking formv id", form.id)
            user2 = CustomUser.objects.filter(email = user)
            print("Usercustom data", [user2[0].id, user2[0].email, user2[0].is_email_verified])
            # send_activation_email(user2[0], request)
            print("send_activation_email completed" )
            # messages.add_message(request, messages.SUCCESS,
                                #  'We sent you an email to verify your account')

            message = "Request is sent to admin(dxcpgtfmautomation@dxc.com)"
            return redirect('query_app:login-page-revert', s = message)
            
        
    context = {
        'form' : form,
    } 
    
    return render(request, 'query_app/register.html', context)

def loginPage_Revert(request, s=""):
    messages.success(request, s) 
    return redirect('query_app:login-page')
    
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email = email, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('query_app:base_html')
        else:
            # messages.info(request, 'Username OR Password is incorrect') 
            messages.error(request, 'Username OR Password is incorrect') 
    
    # else:
    #     # messages.add_message(request, messages.SUCCESS,str)
    #     messages.success(request, s)  
    #     return redirect('query_app:login-page')            
        
    
    return render(request, 'query_app/login.html')


def logoutPage(request):
    logout(request)
    
    return redirect('query_app:login-page')


# --------------------------------------Extract------------------------------------

# def extract (request, id):
#     thread = ReportExtractThread(id)
#     thread.start()
#     thread.join()
#     data = thread.value
#     print(data)
#     #     return data
        
    
    
#     report = Reports.objects.filter(id=id).values()
#     region = Regions.objects.filter(Region=report[0]['Region_id']).values()
#     region_data = Regions.objects.filter(Region=region[0]['Region']).values()
#     report_data = Reports.objects.filter(Region=region[0]['Region']).values()
#     
#     context = {
#         "list" : list,  
#         "region_data" : region_data,
#         "report_data" : report_data,
#         "region":region[0]['Region'],
#         'response' : data
        
#     }
#     # thread.join()
#     print("i am")
#     # return data
#     # return HttpResponse("none")
#     return render(request, 'query_app/Home.html', context)


# -------------testing--------------




# def extract(request, id):
    
#     try:
#         # print("id", id)
#         report_data = Reports.objects.filter(id=id).values()
#         # print("report_data", report_data)
#         # print("sql data", report_data[0]['Sql_Query'])
#         # print("Region_id", report_data[0]['Region_id'])
        
        
#         region_data = Regions.objects.filter(Region=report_data[0]['Region_id']).values()
#         print("region_data", region_data[0]['Region'])
        
        
#         start_time = time.time()
#         print('start_time', start_time)
#         con_str = {
#             'DB_HOST' : region_data[0]['DB_Host'],
#             'PORT' : region_data[0]['DB_Port'],  
#             'DB_USER' : 'ei7850',
#             'DB_PASS' : 'Assist_13',
#             'service' : region_data[0]['DB_Service_Name'],    
#         }
        
#         conn = cx_Oracle.connect('{DB_USER}/{DB_PASS}@{DB_HOST}:{PORT}/{service}'.format(**con_str))
        
#         print("connection established")
        
#         sqlquery = report_data[0]['Sql_Query']
#         df = pd.read_sql(sql = sqlquery, con = conn)
#         print(type(df))
#         # print(df)
#         print("len of data fetched", len(df))
#         print("data fetched")
        
#         data_to_update = Reports.objects.filter(id=id)
#         abc = data_to_update.update(Data_Fetched = df.to_json())
#         print("data inserted ", abc)
        
#         print("before response")
#         response = HttpResponse(content_type = 'text/csv')
#         response['Content-Disposition'] = 'attachment; filename=' +report_data[0]['Report_Name']+' '+ datetime.now().strftime("%d/%b/%Y %H:%M:%S") + '.csv'
#         print("after response")
#         df.to_csv(path_or_buf=response, index=False)
        
        
#         end_time = time.time()
#         print('end_time', end_time)
#         Time_taken = end_time - start_time
        
#         print(type(Time_taken))
#         print("Time taken to extract the file",math.trunc(Time_taken))
        
#         print("response", response)
#         print("response type", type(response))
#         return response
        
#     except Exception as e:
#         print("thread error ", e)
#         messages.error(request, e)
#         # return redirect(reverse('query_app:base_html_region')+region_data[0]['Region'])
#         # return reverse('query_app:base_html_region', kwargs={'slug': region_data[0]['Region']}) 
#         return redirect('query_app:base_html_region', region = region_data[0]['Region'])

# -------------- testing job run and extract seperately ----------------------------
def fetch_data(request, id):
    
    print("data fetch id ", id, type(id))
    task = data_fetch.delay(id)
    print("task ", [task, task.task_id, task.state])
    print("result_task ", [task, task.result, task.state])
    # print("task ", [task])
    # print("result_task ", [task.result])
    
    report_data = Reports.objects.filter(id=id).values()
    report_data.update(Task_Id = task.task_id)
    region_data = Regions.objects.filter(Region=report_data[0]['Region_id']).values()
    
    return redirect('query_app:base_html_region', region = region_data[0]['Region'])
    

def extract(request, id):
    try:
        print("Extraction started")
        report_data = Reports.objects.filter(id=id).values()
        region_data = Regions.objects.filter(Region=report_data[0]['Region_id']).values()
        report_data_fetched = Reports_Data.objects.filter(Report_Name = report_data[0]['Report_Name']).values()
        
        data = report_data_fetched[0]['Data_Fetched']
        print("type ", type(data))
        
        converted_data = json.loads(data)
        # print("converted type ", converted_data)
        
        df = pd.DataFrame.from_dict(converted_data)
        
        print("before response")
        response = HttpResponse(content_type = 'text/csv')
        # print("type od last_run ", [type(report_data[0]['Last_Run'].strftime("%d/%b/%Y %H:%M:%S")), report_data[0]['Last_Run'].strftime("%d/%b/%Y %H:%M:%S")])
        response['Content-Disposition'] = 'attachment; filename=' +report_data[0]['Report_Name']+' '+ report_data[0]['Last_Run'].strftime("%d/%b/%Y %H:%M:%S") + '.csv'
        # response['Content-Disposition'] = 'attachment; filename=' +report_data[0]['Report_Name']+' '+ datetime.now().strftime("%d/%b/%Y %H:%M:%S") + '.csv'

        print("after response")
        df.to_csv(path_or_buf=response, index=False)
        
        return response
        
    except Exception as e:
        print("error in extraction ", e)
        messages.error(request, e)
        return redirect('query_app:base_html_region', region = region_data[0]['Region'])    

    
    

# # ------------------------------------base Html------------------------------------

@login_required(login_url='query_app:login-page')
def base_html_region(request, region):
    # print('q value ', request.GET['q'])
    
    print('q value request', request.GET)
    
    if 'q' in request.GET:
        print('q value and region ', [request.GET['q'], region])
        q = request.GET['q']
        print('q after ', q)
        report_data_f = Reports.objects.filter(Region=region).values()
        print('before report data for search ',len(report_data_f))
        report_data = report_data_f.filter(Report_Name__icontains = q).values()
        print('after report data for search ', len(report_data)) 
    else:    
        report_data = Reports.objects.filter(Region=region).values()
        print("not searching")
    
    region_data = Regions.objects.filter(Region=region).values()
    
    context = {
        "list" : list,  
        "region_data" : region_data,
        "report_data" : report_data,
        "region":region_data[0]['Region'],
        
        
    }
    
    return render(request, 'query_app/Home.html', context)



def j_serial(o):     # self contained
    from datetime import datetime, date
    return str(o).split('.')[0] if isinstance(o, (datetime, date)) else None


# Ajax call for Last Run data
def get_Ajax_LastRun(request,id):
    print("inside ajax last run view")
    report = Reports.objects.filter(id=id).values()
    lastRun = report[0]['Last_Run']
    print("ajax last run ", lastRun, type(lastRun))
    print("ajax last run json load ", lastRun, type(lastRun), j_serial(lastRun))
    return JsonResponse({"lastRun":j_serial(lastRun)})

# def get_Ajax_LastRun(request):
#     print("inside ajax last run view")
#     report = Reports.objects.all()
    
#     return JsonResponse({"lastRun":list(report)})


# @login_required(login_url='query_app:login-page')
# def base_html_region(request, region):

#     report_data = Reports.objects.filter(Region=region).values()    
#     region_data = Regions.objects.filter(Region=region).values()
#     
#     # print("region", region_data[0]['Region'])
    
#     context = {
#         "list" : list,  
#         "region_data" : region_data,
#         "report_data" : report_data,
#         "region":region_data[0]['Region'],
        
#     }
    
#     return render(request, 'query_app/Home.html', context)



@login_required(login_url='query_app:login-page')
def base_html(request):
    
    context = {
        "list" : list,
        
        
    }
    return render(request, 'query_app/about_RG.html', context)

    




# ----------------------------------------Manage Regions----------------------------------------------------

@login_required(login_url='query_app:login-page')
def list_regions(request, region =''):
    
    list = Regions.objects.all()
    list_R = Reports.objects.all()
    
    if request.method == "GET":
        print("get id", region)
        if region=='':
            form=RegionsForm()
        else:
            r = Regions.objects.get(pk=region)
            form = RegionsForm(instance=r)
         
        # for searching      
        if 'q' in request.GET:
            print('q value and region ', [request.GET['q'], region])
            q = request.GET['q']
            print('q after ', q)
            list = Regions.objects.filter(Region__icontains = q).values()
            print('after report data for search ', len(list)) 
        else:    
            
            print("not searching")
        
          
        context = {
        "form" : form,
        "list_R" : list_R,
        "list" : list,
        
        }
        
        return render(request, 'query_app/Manage_Region copy.html', context)
    else:
        print("post id", region)
        if region == '':
            form = RegionsForm(request.POST)
        else:
            r = Regions.objects.get(pk=region)
            form = RegionsForm(request.POST or None, instance=r) 
            
        if form.is_valid():
            print()
            form.save()
        return redirect('query_app:manage_regions')
    
@login_required(login_url='query_app:login-page')   
def delete_region(request, region):
    print("delete id", region)
    region_delete = Regions.objects.get(pk=region)
    region_delete.delete()
    return redirect('query_app:manage_regions')
    



# --------------------------------------------Manage Reports--------------------------------------

@login_required(login_url='query_app:login-page')
def list_reports(request, id=0):
    
    
    
    list_R = Reports.objects.all()
    
    if request.method == "GET":
        print("get id", id)
        if id==0:
            form=ReportsForm()
        else:
            report = Reports.objects.get(pk=id)
            form = ReportsForm(instance=report)
            
        # for searching      
        if 'q' in request.GET:
            print('q value and region ', [request.GET['q']])
            q = request.GET['q']
            print('q after ', q)
            list_R = Reports.objects.filter(Report_Name__icontains = q).values()
            print('after report data for search ', len(list)) 
        else:    
            list_R = Reports.objects.all()
            print("not searching")
                
        context = {
        "form" : form,
        "list_R" : list_R,
        "list" : list,
        
        }
        
        return render(request, 'query_app/Manage_Reports.html', context)
    else:
        print("post id", id)
        if id == 0:
            form = ReportsForm(request.POST)
        else:
            report = Reports.objects.get(pk=id)
            form = ReportsForm(request.POST or None, instance=report) 
            
        if form.is_valid():
            print()
            form.save()
        return redirect('query_app:manage_reports')
    
@login_required(login_url='query_app:login-page')        
def delete_report(request, id):
    print("delete id", id)
    report_delete = Reports.objects.get(pk=id)
    report_delete.delete()
    return redirect('query_app:manage_reports')



# ----------------------------------------Manage Users----------------------------------------------------

@login_required(login_url='query_app:login-page')
def list_users(request, id =0):    
    print("request get ", request.GET)
    
    users = CustomUser.objects.all()
    
    list_R = Reports.objects.all()
    is_edit = False
    # print(users)
    
    if request.method == "GET":
        print("get id", id)
        if id==0:
            form=CustomUserCreationForm()
            # print('form_userList', form)
        else:
            is_edit = True
            print(" inside else of get is_edit", is_edit)
            u = CustomUser.objects.get(id=id)
            form = CustomUserChangeForm(instance=u)
            print(" yes get form", [form.fields, form.fields['email'], type(form.fields['email']) ,type(form)])
            
        # for searching      
        if 'q' in request.GET:
            
            print('q value and region ', [request.GET['q']])
            q = request.GET['q']
            print('q after ', q)
            users = CustomUser.objects.filter(email__icontains = q)
            print('after report data for search ', len(list)) 
        else:    
            users = CustomUser.objects.all()
            print("not searching")
        
        print(" in get is_edit", is_edit)       
        context = {
        "form" : form,
        "list_R" : list_R,
        "list" : list,
        "users" : users,
        "is_edit" : is_edit,
        }
        
        return render(request, 'query_app/Manage_Users.html', context)
    else:
        print("post id", id)
        if id == 0:
            form = CustomUserCreationForm(request.POST)
            
            if form.is_valid():
                print()
                form.save()
                form.save_m2m()

            else:
                context = {
                    "form" : form,
                    "list_R" : list_R,
                    "list" : list,
                    "users" : users,
                    "is_edit" : is_edit,

                }
                return render(request, 'query_app/Manage_Users.html', context )
        else:
            u = CustomUser.objects.get(id=id)
            form = CustomUserChangeForm(request.POST or None, instance=u) 
            print('edited user', u)
            print('edited user form', form.errors)
            
            if form.is_valid():
                print()
                form.save(commit=False)  
                form.save_m2m()
                form.save()
                          
            
            else:
                context = {
                    "form" : form,
                    "list_R" : list_R,
                    "list" : list,
                    "users" : users,
                    "is_edit" : is_edit,   

                }
                return render(request, 'query_app/Manage_Users.html', context )
            
        
        return redirect('query_app:manage_users')
    
@login_required(login_url='query_app:login-page')   
def delete_user(request, id):
    print("delete id", id)
    user = CustomUser.objects.get(pk=id)
    user.delete()
    return redirect('query_app:manage_users')


def pending_user_request(request):

    # for searching      
    if 'q' in request.GET:
        
        print('q value and region ', [request.GET['q']])
        q = request.GET['q']
        print('q after ', q)
        pending_user = CustomUser.objects.filter(email__icontains = q, is_active = False)
    else:    
        pending_user = CustomUser.objects.filter(is_active = False)
        print("not searching")
    
    context = {
        "list" : list,
        "pending_user" : pending_user,
    }
    
    return render(request, 'query_app/pending_User_Request.html', context)

def accept_user_request(request, id):
    user = CustomUser.objects.filter(id = id)
    user.update(is_active = True)
    return redirect('query_app:pending_user_request')


def reject_user_request(request, id):
    user = CustomUser.objects.get(pk=id)
    user.delete()
    return redirect('query_app:pending_user_request')


# ----------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------
