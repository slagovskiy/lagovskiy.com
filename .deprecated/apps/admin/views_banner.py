from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from apps.statistic.models import *
from apps.banner.models import Banner
from apps.admin.utils import *
from apps.admin.views import custom_proc


def banner_index(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/banner/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def banner_getall(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    banners = []
    try:
        banners = Banner.objects.all()
    except:
        logging.exception('Error get categories list')
    t = loader.get_template('admin/banner/banner_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'banners': banners,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def banner_getlist(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    banners = []
    try:
        banners = Banner.objects.all().filter(deleted=False)
    except:
        logging.exception('Error get banners list')
    t = loader.get_template('admin/banner/banner_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'banners': banners,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def banner_edit(request, baner_id):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    banner = None
    try:
        if id != 0:
            banner = Banner.objects.get(id=baner_id)
    except:
        logging.exception('Error get category item')
    t = loader.get_template('admin/banner/banner_edit.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'banner': banner,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def banner_save(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    try:
        tmp_id = request.POST.get('_id', 0)
        tmp_name = request.POST.get('_name', '')
        tmp_slug = request.POST.get('_slug', '')
        tmp_code = request.POST.get('_code', '')
        tmp_sort = request.POST.get('_sort', 100)
        tmp_deleted = request.POST.get('_deleted', False)
        tmp_hidden = request.POST.get('_hidden', False)
        logging.warning(tmp_deleted)
        logging.warning(tmp_hidden)
        if tmp_name == '':
            tmp_name = 'qwerty'
        if tmp_slug == '':
            tmp_slug = 'qwerty'
        if tmp_sort == '':
            tmp_sort = 1000
        if tmp_id != '':
            banner = Banner.objects.get(id=tmp_id)
            banner.slug = tmp_slug
            banner.name = tmp_name
            banner.code = tmp_code
            banner.sort = tmp_sort
            if tmp_deleted == "True":
                banner.deleted = True
            else:
                banner.deleted = False
            if tmp_hidden == "True":
                banner.hidden = True
            else:
                banner.hidden = False
            banner.save()
        else:
            banner = Banner.objects.create(
                slug=tmp_slug,
                name=tmp_name,
                code=tmp_code,
                sort=tmp_sort,
            )
            if tmp_deleted == "True":
                banner.deleted = True
            else:
                banner.deleted = False
            if tmp_hidden == "True":
                banner.hidden = True
            else:
                banner.hidden = False
            banner.save()
    except:
        logging.exception('Error save or add banner')
    return HttpResponseRedirect('/admin/banner/')