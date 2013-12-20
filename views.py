# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout

import logging
from utils.capcha import captcha_image, capcha_code

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
    '''
    message = ''
    t = loader.get_template('default.html')
    c = RequestContext(
        request,
            {
            'message': message,
            },
        processors=[custom_proc]
    )
    return HttpResponse(t.render(c))
    '''
    return HttpResponseRedirect('/blog/')

def capcha(request):
    return captcha_image(capcha_code(4), 1)
