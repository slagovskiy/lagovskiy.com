# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

from settings import *

urlpatterns = patterns('',
    url(r'^$', 'views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('apps.blog.urls')),
)

# static urls will be disabled in production mode
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
