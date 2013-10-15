# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q

from datetime import date
from datetime import timedelta
from datetime import datetime

import logging

from apps.blog.models import *
from apps.blog.settings import *

from django.utils import feedgenerator

def custom_proc(request):
    return {
        'app_title': 'RSS',
        'link_app': 'rss',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

def index(request):
    feed = feedgenerator.Rss201rev2Feed(
        title=u"Poynter E-Media Tidbits",
        link=u"http://www.poynter.org/column.asp?id=31",
        description=u"A group Weblog by the sharpest minds in online media/journalism/publishing.",
        language=u"en",
    )
    feed.add_item(
        title="Hello",
        link=u"http://www.holovaty.com/test/",
        description="Testing."
    )
    t = loader.get_template('ajax.html')
    c = RequestContext(
        request,
        {
            'data': '<?xml version="1.0" encoding="utf-8"?><rss><channel></channel></rss>'#feed.writeString(encoding="utf-8"),
            },
        processors=[custom_proc])
    return HttpResponse(t.render(c))

def postby_tag(request, tag):
    pass


def postby_category(request, category):
    pass

def comment(request, post_id):
    pass