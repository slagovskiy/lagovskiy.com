from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.admin.views.index'),
    url(r'^login/$', 'apps.admin.views.login'),
)


