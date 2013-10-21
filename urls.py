# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.generic.simple import direct_to_template

from utils.rss import *

admin.autodiscover()

from settings import *

urlpatterns = patterns('',
    url(r'^$', 'views.index'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    url(r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),

    # RSS
    url(r'^rss/', DefaultRSS()),
    url(r'^rss/tag/(?P<tag>[-\w]+)/$', TagRSS()),
    url(r'^rss/category/(?P<category>[-\w]+)/$', CategoryRSS()),
    url(r'^rss/comments/(?P<post>[-\w]+)/$', CommentsRSS()),

    # ATOM
    url(r'^atom/', DefaultAtom()),
    url(r'^atom/tag/(?P<tag>[-\w]+)/$', TagAtom()),
    url(r'^atom/category/(?P<category>[-\w]+)/$', CategoryAtom()),
    url(r'^atom/comments/(?P<post>[-\w]+)/$', CommentsAtom()),

    url(r'^blog/', include('apps.blog.urls')),
    url(r'^projects/', include('apps.projects.urls')),
    url(r'^about/', include('apps.about.urls')),

    url(r'^djadmin/', include(admin.site.urls)),
    url(r'^admin/', include('apps.admin.urls')),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

# static urls will be disabled in production mode
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
