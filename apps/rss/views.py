# -*- coding: utf-8 -*-
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
        'app_title': 'RSS',
        'link_app': 'rss',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

def index(request):
    pass

def postby_tag(request, tag):
    pass


def postby_category(request, category):
    pass

def comment(request, post_id):
    pass