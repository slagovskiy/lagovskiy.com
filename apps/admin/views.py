from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q

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
        'user': request.session.get('user', None),
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

def login(request):
    message = ''
    t = loader.get_template('admin/login.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))
