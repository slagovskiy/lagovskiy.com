from django.conf.urls.defaults import patterns, include, url
from apps.rss.views import *

urlpatterns = patterns('',
    url(r'^$', DefaultAtom()),
    url(r'^tag/(?P<tag>[-\w]+)/$', TagAtom()),
    url(r'^category/(?P<category>[-\w]+)/$', CategoryAtom()),
    url(r'^comments/(?P<post>[-\w]+)/$', CommentsAtom()),
)

