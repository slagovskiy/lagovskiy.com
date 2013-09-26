# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout

import logging

def custom_proc(request):
    return {
        'app_title': '',
        'link_app': 'home',
        #'link_category': '',
        #'link_tag': '',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

def index(request):
    message = ''

    log = logging.getLogger('odyssey')
    log.debug("it's debug")
    log.info("it's info")
    log.warn("it's warn")
    log.error("it's error")
    logging.debug('1234567')

    t = loader.get_template('default.html')
    c = RequestContext(
        request,
            {
            'message': message,
            },
        processors=[custom_proc]
    )
    return HttpResponse(t.render(c))
