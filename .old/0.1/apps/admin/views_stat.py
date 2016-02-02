from urllib2 import unquote
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

import logging
from apps.admin.utils import *
from apps.admin.views import custom_proc
from apps.statistic.models import Visitor


def stat_index(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/statistic/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def stat_by_point(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    visitors = []
    try:
        visitors = Visitor.objects.all() \
            .values('point').annotate(cnt=Count('point')).order_by('point')
    except:
        logging.exception('Error get visitors list')
    t = loader.get_template('admin/statistic/points_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'visitors': visitors,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def stat_by_point_date(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    visitors = []
    try:
        visitors = Visitor.objects.all()\
            .filter(point=unquote(request.GET.get('p', '')))\
            .values('day').annotate(cnt=Count('day'))
            #.values_list('day').order_by('-day').distinct()
    except:
        logging.exception('Error get visitors list')
    t = loader.get_template('admin/statistic/pointsdate_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'visitors': visitors,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def stat_by_point_date_list(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    visitors = []
    try:
        visitors = Visitor.objects.all().filter(point=unquote(request.GET.get('p', '')),
                                                day=unquote(request.GET.get('d', ''))).order_by('date')
    except:
        logging.exception('Error get visitors list')
    t = loader.get_template('admin/statistic/pointsdatelist_all.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'visitors': visitors,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))