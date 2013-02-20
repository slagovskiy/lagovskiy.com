from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.blog.views.index'),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'apps.blog.views.postby_tag'),
    url(r'^category/(?P<category>[-\w]+)/$', 'apps.blog.views.postby_category'),
    url(r'^view/(?P<slug>[-\w]+)/$', 'apps.blog.views.post_view'),
    url(r'^comment/bypost/(?P<post_id>[-\w]+)/$', 'apps.blog.views.comment_bypost'),
    url(r'^comment/save/(?P<id>[-\w]+)/$', 'apps.blog.views.comment_save'),
)

