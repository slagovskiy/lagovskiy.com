from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.rss.index'),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'apps.rss.postby_tag'),
    url(r'^category/(?P<category>[-\w]+)/$', 'apps.rss.postby_category'),
    url(r'^/comment/(?P<post_id>[-\w]+)/$', 'apps.rss.comment'),
)

