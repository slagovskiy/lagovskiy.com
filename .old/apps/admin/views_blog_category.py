from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

import logging

from apps.blog.models import Category
from apps.admin.utils import *
from apps.admin.views import custom_proc


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
        logging.exception('Error get categories list')
    t = loader.get_template('admin/blog/category_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'categories': categories,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def blog_category_getlist(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    categories = []
    try:
        categories = Category.objects.all().filter(deleted=False)
    except:
        logging.exception('Error get categories list')
    t = loader.get_template('admin/blog/category_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'categories': categories,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def blog_category_edit(request, category_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    category = None
    try:
        if category_id != 0:
            category = Category.objects.get(id=category_id)
    except:
        logging.exception('Error get category item')
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
    try:
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_slug = request.POST.get('_slug', '')
        tmp_sort = request.POST.get('_sort', 100)
        tmp_deleted = request.POST.get('_deleted', False)
        if tmp_name == '':
            tmp_name = 'qwerty'
        if tmp_slug == '':
            tmp_slug = 'qwerty'
        if tmp_sort == '':
            tmp_sort = 1000
        logging.warning(tmp_id)
        if tmp_id != '':
            category = Category.objects.get(id=tmp_id)
            category.slug = tmp_slug
            category.name = tmp_name
            category.sort = tmp_sort
            if tmp_deleted == "True":
                category.deleted = True
            else:
                category.deleted = False
            category.save()
        else:
            category = Category.objects.create(
                slug=tmp_slug,
                name=tmp_name,
                sort=tmp_sort,
            )
            if tmp_deleted == "True":
                category.deleted = True
            else:
                category.deleted = False
            category.save()
    except:
        logging.exception('Error save or add category')
    return HttpResponseRedirect('/admin/blog/category/')


def blog_category_moveup(request, category_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    try:
        categories = Category.objects.all()
        category_prev = None
        for category in categories:
            if category.id == int(category_id):
                if category_prev:
                    tmp = category.sort
                    category.sort = category_prev.sort
                    category_prev.sort = tmp
                    category.save()
                    category_prev.save()
            category_prev = category
    except:
        logging.exception('Error move up category')
    return HttpResponseRedirect('/admin/blog/category/')


def blog_category_movedown(request, category_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    try:
        categories = Category.objects.all()
        category_prev = None
        for category in reversed(categories):
            if category.id == int(category_id):
                if category_prev:
                    tmp = category.sort
                    category.sort = category_prev.sort
                    category_prev.sort = tmp
                    category.save()
                    category_prev.save()
            category_prev = category
    except:
        logging.exception('Error move up category')
    return HttpResponseRedirect('/admin/blog/category/')