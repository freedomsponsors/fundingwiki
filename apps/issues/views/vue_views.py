# Create your views here.

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.http.response import HttpResponse
from django.template import  RequestContext
from django.shortcuts import render, redirect, resolve_url
from apps.issues.services import issue_services
from apps.issues.services.mail_services import *
from apps.issues.services import stats_services
from django.contrib import messages
import logging
from apps.issues.services import testmail_service
# from apps.issues.views import HOME_CRUMB
from django.contrib.auth import authenticate, login as auth_login


logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'vue/home.html',{})