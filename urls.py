# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.generic.simple import direct_to_template

admin.autodiscover()

from settings import *

urlpatterns = patterns('',
    url(r'^$', 'views.index'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    url(r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),

    url(r'^blog/', include('apps.blog.urls')),
    url(r'^projects/', include('apps.projects.urls')),
    url(r'^about/', include('apps.about.urls')),

    url(r'^djadmin/', include(admin.site.urls)),
    url(r'^admin/', include('apps.admin.urls')),
)

# static urls will be disabled in production mode
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
