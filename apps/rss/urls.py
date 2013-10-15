from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.rss.views.index'),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'apps.rss.views.postby_tag'),
    url(r'^category/(?P<category>[-\w]+)/$', 'apps.rss.views.postby_category'),
    url(r'^/comment/(?P<post_id>[-\w]+)/$', 'apps.rss.views.comment'),
)

