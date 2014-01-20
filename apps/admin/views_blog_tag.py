from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

from apps.blog.models import *
from apps.statistic.models import *
from apps.admin.utils import *
from apps.admin.views import custom_proc


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
        logging.exception('Error get tags list')
    t = loader.get_template('admin/blog/tag_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'tags': tags,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def blog_tag_getlist(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    tags = []
    try:
        tags = Tag.objects.all().filter(deleted=False)
    except:
        logging.exception('Error get tags list')
    t = loader.get_template('admin/blog/tag_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'tags': tags,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def blog_tag_edit(request, tag_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    tag = None
    try:
        if tag_id != 0:
            tag = Tag.objects.get(id=tag_id)
    except:
        logging.exception('Error get tag item')
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
    try:
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_slug = request.POST.get('_slug', '')
        tmp_sort = request.POST.get('_sort', 100)
        tmp_deleted = request.POST.get('_deleted', False)
        if tmp_slug == '':
            tmp_slug = 'qwerty'
        if tmp_name == '':
            tmp_name = 'qwerty'
        if tmp_sort == '':
            tmp_sort = 1000
        logging.warning(tmp_id)
        if tmp_id != '':
            tag = Tag.objects.get(id=tmp_id)
            tag.slug = tmp_slug
            tag.name = tmp_name
            tag.sort = tmp_sort
            if tmp_deleted == "True":
                tag.deleted = True
            else:
                tag.deleted = False
            tag.save()
        else:
            tag = Tag.objects.create(
                slug=tmp_slug,
                name=tmp_name,
                sort=tmp_sort,
            )
            if tmp_deleted == "True":
                tag.deleted = True
            else:
                tag.deleted = False
            tag.save()
    except:
        logging.exception('Error save or add tag')
    return HttpResponseRedirect('/admin/blog/tag/')


def blog_tag_moveup(request, tag_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    try:
        tags = Tag.objects.all()
        tag_prev = None
        for tag in tags:
            if tag.id == int(tag_id):
                if tag_prev:
                    tmp = tag.sort
                    tag.sort = tag_prev.sort
                    tag_prev.sort = tmp
                    tag.save()
                    tag_prev.save()
            tag_prev = tag
    except:
        logging.exception('Error move up tag')
    return HttpResponseRedirect('/admin/blog/tag/')


def blog_tag_movedown(request, tag_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    try:
        tags = Tag.objects.all()
        tag_prev = None
        for tag in reversed(tags):
            if tag.id == int(tag_id):
                if tag_prev:
                    tmp = tag.sort
                    tag.sort = tag_prev.sort
                    tag_prev.sort = tmp
                    tag.save()
                    tag_prev.save()
            tag_prev = tag
    except:
        logging.exception('Error move up tag')
    return HttpResponseRedirect('/admin/blog/tag/')