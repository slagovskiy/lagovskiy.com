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
        'app_title': 'Blog',
        'link_app': 'blog',
        #'link_category': '',
        #'link_tag': '',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

def index(request):
    message = ''
    posts = []
    try:
        posts = Post.objects.all().filter(status=2)
    except:
        logging.exception('Error get posts list')
    t = loader.get_template('blog/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'posts': posts,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def post_view(request, slug):
    message = ''
    post = None
    try:
        post = Post.objects.all().filter(slug=slug)[0]
    except:
        logging.exception('Error get post')
    t = loader.get_template('blog/post_view.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'post': post,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))
