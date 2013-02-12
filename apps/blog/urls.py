from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.blog.views.index'),
    url(r'^view/(?P<slug>[-\w]+)/$', 'apps.blog.views.post_view'),
)

