from django.core.context_processors import request
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
from apps.blog.admin import CategoryAdmin

from apps.blog.models import *
from apps.blog.settings import *

from apps.blog.models import Category

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

# utils

def check_access(user, access):
    try:
        if not getattr(user.get_profile(), access)():
            return False
        else:
            return True
    except:
        return False


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

# login / logout

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

def ad(request):
    message = ''
    t = loader.get_template('admin/access_denied.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

# blog

## blog: category

def blog_category(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/blog/category.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_category_getall(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    categories = []
    try:
        categories = Category.objects.all()
    except:
        logging.error('Error get categories list')
    t = loader.get_template('admin/blog/category_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'categories': categories,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_category_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    category = None
    try:
        if id!=0:
            category = Category.objects.get(id=id)
    except:
        logging.error('Error get category item')
    t = loader.get_template('admin/blog/category_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'category': category,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_category_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        category = None
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_slug = request.POST.get('_slug', '')
        tmp_sort = request.POST.get('_sort', 100)
        tmp_deleted = request.POST.get('_deleted', False)
        logging.warning(tmp_id)
        if tmp_id!='':
            category = Category.objects.get(id=tmp_id)
            category.slug = tmp_slug
            category.name = tmp_name
            category.sort = tmp_sort
            if tmp_deleted=="True":
                category.deleted = True
            else:
                category.deleted = False
            category.save()
        else:
            category = Category.objects.create(
                slug = tmp_slug,
                name = tmp_name,
                sort = tmp_sort,
            )
            if tmp_deleted=="True":
                category.deleted = True
            else:
                category.deleted = False
            category.save()
    except:
        logging.exception('Error save or add category')
    return  HttpResponseRedirect('/admin/blog/category/')


## blog: tag

def blog_tag(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/blog/tag.html')
    c = RequestContext(
        request,
        {
            'message': message,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_tag_getall(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    tags = []
    try:
        tags = Tag.objects.all()
    except:
        logging.error('Error get tags list')
    t = loader.get_template('admin/blog/tag_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'tags': tags,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_tag_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    tag = None
    try:
        if id!=0:
            tag = Tag.objects.get(id=id)
    except:
        logging.error('Error get tag item')
    t = loader.get_template('admin/blog/tag_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'tag': tag,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def blog_tag_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    try:
        category = None
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_slug = request.POST.get('_slug', '')
        tmp_sort = request.POST.get('_sort', 100)
        tmp_deleted = request.POST.get('_deleted', False)
        logging.warning(tmp_id)
        if tmp_id!='':
            tag = Tag.objects.get(id=tmp_id)
            tag.slug = tmp_slug
            tag.name = tmp_name
            tag.sort = tmp_sort
            if tmp_deleted=="True":
                tag.deleted = True
            else:
                tag.deleted = False
            tag.save()
        else:
            tag = Tag.objects.create(
                slug = tmp_slug,
                name = tmp_name,
                sort = tmp_sort,
            )
            if tmp_deleted=="True":
                tag.deleted = True
            else:
                tag.deleted = False
            tag.save()
    except:
        logging.exception('Error save or add tag')
    return  HttpResponseRedirect('/admin/blog/tag/')

## post

def blog_post_edit(request, id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    post = None
    try:
        if id!=0:
            post = Post.objects.get(id=id)
    except:
        logging.error('Error get post item')
    t = loader.get_template('admin/blog/post_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'post': post,
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))
