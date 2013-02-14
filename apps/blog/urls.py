from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.blog.views.index'),
    url(r'^view/(?P<slug>[-\w]+)/$', 'apps.blog.views.post_view'),
    url(r'^comment/bypost/(?P<post_id>[-\w]+)/$', 'apps.blog.views.comment_bypost'),
    url(r'^comment/save/$', 'apps.blog.views.comment_save'),
)

