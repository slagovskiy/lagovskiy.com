from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from datetime import date
from datetime import timedelta
from datetime import datetime

import logging

from apps.blog.models import *
from apps.blog.settings import *

def custom_proc(request):
    return {
        'app_title': 'Admin',
        'link_app': 'admin',
        #'link_category': '',
        #'link_tag': '',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

def index(request):
    message = ''
    t = loader.get_template('admin/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def login_action(request):
    message = ''
    t = loader.get_template('admin/login.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def login_check(request):
    _login = request.POST.get('txtLogin', '')
    _password = request.POST.get('txtPassword', '')
    logging.warning(_login)
    logging.warning(_password)
    page = request.POST.get('return', '/')
    if page == None:
        page = '/'
    user = authenticate(username=_login, password=_password)
    logging.warning(user)
    if user is not None:
        if user.is_active:
            login(request, user)
    return HttpResponseRedirect(page)

def logout_action(request):
    page = request.META.get('HTTP_REFERER')
    if page == None:
        page = '/'
    logout(request)
    return HttpResponseRedirect(page)
