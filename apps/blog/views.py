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
    page = int(request.GET.get('page', 1))
    try:
        posts = Post.objects.all().filter(status=Post.PUBLISHED_STATUS).order_by('-sticked', '-published')
        paginator = Paginator(posts, PAGE_SIZE)
        if page<=0:
            page = 1
        if page>paginator.num_pages:
            page = paginator.num_pages
    except:
        logging.exception('Error get posts list')
    t = loader.get_template('blog/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'posts': paginator.page(page),
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def postby_tag(request, tag):
    message = ''
    posts = []
    tags = None
    page = int(request.GET.get('page', 1))
    try:
        tags = Tag.objects.get(slug=tag)
        posts = Post.objects.all().filter(status=Post.PUBLISHED_STATUS, tags=tags).order_by('-sticked', '-published')
        paginator = Paginator(posts, PAGE_SIZE)
        if page<=0:
            page = 1
        if page>paginator.num_pages:
            page = paginator.num_pages
    except:
        logging.exception('Error get posts list')
    t = loader.get_template('blog/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'posts': paginator.page(page),
            'tags': tags,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def postby_category(request, category):
    message = ''
    posts = []
    categories = None
    page = int(request.GET.get('page', 1))
    try:
        categories = Category.objects.get(slug=category)
        posts = Post.objects.all().filter(status=Post.PUBLISHED_STATUS, categories=categories).order_by('-sticked', '-published')
        paginator = Paginator(posts, PAGE_SIZE)
        if page<=0:
            page = 1
        if page>paginator.num_pages:
            page = paginator.num_pages
    except:
        logging.exception('Error get posts list')
    t = loader.get_template('blog/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'posts': paginator.page(page),
            'link_category': categories,
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
    if post:
        if post.status==Post.HIDDEN_STATUS or post.status==Post.PUBLISHED_STATUS:
            t = loader.get_template('blog/post_view.html')
            c = RequestContext(
                request,
                {
                    'message': message,
                    'post': post,
                    },
                processors=[custom_proc])
            return HttpResponse(t.render(c))
        else:
            HttpResponseRedirect('/blog/')
    return HttpResponseRedirect('/blog/')
