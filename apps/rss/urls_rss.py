from django.conf.urls.defaults import patterns, include, url
from apps.rss.views import *

urlpatterns = patterns('',
    url(r'^$', DefaultRSS()),
    url(r'^tag/(?P<tag>[-\w]+)/$', TagRSS()),
    url(r'^category/(?P<category>[-\w]+)/$', CategoryRSS()),
    url(r'^comments/(?P<post>[-\w]+)/$', CommentsRSS()),
)

