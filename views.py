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
        'link_category': '',
        'link_tag': '',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

def index(request):
    message = ''
    logging.warning(request.user)
    t = loader.get_template('default.html')
    c = RequestContext(
        request,
            {
            'message': message,
            },
        processors=[custom_proc]
    )
    return HttpResponse(t.render(c))
