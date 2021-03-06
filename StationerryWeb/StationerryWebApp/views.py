from django.shortcuts import render

# for user authentication, login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

# for @login_required
from django.contrib.auth.decorators import login_required

# reference the Users model for user registration
from django.contrib.auth.models import User
from .models import App
from .models import BugReport

# import utilities.py
from StationerryBackend.utilities import *

import datetime
# from datetime import date, timedelta

# for top 5 errors
from django.db.models import Count
import json

""" 
Create your views here.
Views are referenced by StationerryWebApp.urls
"""

LOGIN_URL = '/login/'
LOGIN_TEMPLATE = 'stationerry/login.html'
DASH_TEMPLATE = 'stationerry/dashboard.html'
ERRORS_TEMPLATE = 'stationerry/errors.html'
REGISTER_TEMPLATE = 'stationerry/register.html'
PROJECTS_TEMPLATE = 'stationerry/projects.html'
INFO_TEMPLATE = 'stationerry/info.html'
ACCOUNT_TEMPLATE = 'stationerry/account.html'

# This is the homepage
def home(request):
    return render(request, LOGIN_TEMPLATE, {})

# This is for the user sign up / registration
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']


    	User.objects.create (
            first_name = name,
            username = username,
            password = password,
            email = email
        )


        # this fixes the password issue because
        # set_password(raw_input) hashes the raw input passed in
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

        return HttpResponse('New user created.')



    return render(request, REGISTER_TEMPLATE, {})

# This is the user authentication 
def userLogin(request):
    errMessage = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # check if user is in our userbase
        if user is not None:
            # in the Django admin thingy, there's a tick mark for (in)activeness
            # if user is inactive, can't log in
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/dashboard/")

            else:
                errMessage = "Your account is deactivated."

        else:
            errMessage = "Invalid username or password."

    # first param is the request, second is the template, third is a variable to be passed to template
    return render(request, LOGIN_TEMPLATE, {"errMessage":errMessage})

def userLogout(request):
    logout(request)
    return HttpResponseRedirect(LOGIN_URL)

# This is the main page after the user logs in.
@login_required
def dashboard(request):
    now = datetime.datetime.now()
    monthName = now.strftime("%b")
    day = str(now.day)
    year = str(now.year) 

    # errors from today
    todayErrors = len(getTimeErrors(now.strftime("%Y-%m-%d"), request.user))
    totalErrors = len(getAllErrors("Exception", request.user))
    uniqueErrors = len(getUniqErrors(request.user))

    #top5 = getTop5(request.user)
    top5List = json.dumps(getTop5(request.user))
    weeklyList = json.dumps(getErrorsByDay(request.user))

    return render(request, DASH_TEMPLATE, {'monthName' : monthName, 'day':day, 'year': year,
                                            'totalErrors':totalErrors, 'todayErrors': todayErrors, 'uniqueErrors':uniqueErrors,
                                            'top5List' : top5List, 'weeklyList':weeklyList})

@login_required
def errors(request):
    errorList = []
    searchQuery = ""
    hideResults = True

    # default search
    if 'q' in request.GET:
        # check if the GET request named 'q' has an empty value
        if request.GET['q'] == '':
            print 'ERRORS.HTML: Nothing was entered.' 
            hideResults = True
        # if not empty, probabably a valid search query. fetch all matching
        # results from db in a list of dictionaries
        else:
            print 'ERRORS.HTML: You searched for ' + request.GET['q']

            errorList = getAllErrors(request.GET['q'], request.user)

            hideResults = False
            searchQuery = request.GET['q']

    elif 'fq' in request.GET:
        if request.GET['fq'] == '':
            print 'ERRORS.HTML: Nothing was entered.'
            hideResults = True
        else:
            print 'ERRORS.HTML: You filtered for ' + request.GET['fq']
            
            errorList = errorFilters(request.GET['fq'], request.GET['errorType'], request.GET['appName'], request.GET['appVersion'], request.GET['os'], request.GET['deviceModel'], request.user)
            hideResults = False
            searchQuery = request.GET['fq']

    return render(request, ERRORS_TEMPLATE, {"errorList" : errorList, "hideResults" : hideResults, "searchQuery" : searchQuery})

@login_required
def projects(request):

    if request.method == 'POST':
        name = request.POST['name']
        version = request.POST['version']
        platform = request.POST['platform']
        
        App.objects.create (
            App_Name=name,
            App_Version=version,
            Platform=platform,
            username=request.user
        )

    # obtain the user's projects
    querySet = App.objects.filter(username=request.user.id)

    # turn the query set into a list for the template
    stationList = []
    for app in querySet:
        stationList.append(app)
    
    return render(request, PROJECTS_TEMPLATE, {"stationList" : stationList})

@login_required
def info(request):
    return render(request, INFO_TEMPLATE, {})

@login_required
def account(request):
    user = User.objects.get(username=request.user)

    username = user.username
    name = user.first_name + ' ' + user.last_name
    email = user.email
    date_joined = user.date_joined
    last_login = user.last_login

    return render(request, ACCOUNT_TEMPLATE, {'username' : username, 'name':name, 'email':email, 'date_joined':date_joined, 'last_login': last_login})
