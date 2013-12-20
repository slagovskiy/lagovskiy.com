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
    return HttpResponseRedirect('/blog/')

def capcha(request):
    request.session['CAPCHA_CODE'] = capcha_code(4)
    return captcha_image(request.session['CAPCHA_CODE'], 1)


def capcha_check(request, code):
    data = '0'
    if request.session['CAPCHA_CODE'] == str(code).upper():
        return HttpResponse('1', content_type="application/javascript")#data = '1'
    else:
        return HttpResponse('0', content_type="application/javascript")#data = '0'
    #t = loader.get_template('ajax.html')
    #c = RequestContext(
    #    request,
    #    {
    #        'data': data,
    #        },
    #    processors=[custom_proc])
    #return HttpResponse(t.render(c))
