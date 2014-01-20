from urllib2 import unquote
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

import logging

from apps.admin.utils import *
from apps.admin.views import custom_proc
from apps.statistic.models import Visitor


def blog_visitors_by_point(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    visitors = []
    try:
        visitors = Visitor.objects.all().filter(point=unquote(request.GET.get('p', '')),
                                                day=unquote(request.GET.get('d', ''))).order_by('date')
    except:
        logging.exception('Error get visitors list')
    t = loader.get_template('admin/statistic/visitors_getall.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'visitors': visitors,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def blog_visitors_dates(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    visitors = []
    try:
        visitors = Visitor.objects.all() \
            .filter(point=unquote(request.GET.get('p', ''))) \
            .values_list('day').order_by('-day').distinct()
    except:
        logging.exception('Error get visitors list')
    t = loader.get_template('admin/statistic/visitors_dates.html')
    c = RequestContext(
        request,
        {
            'message': message,
            'visitors': visitors,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))