from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.admin.views.index'),
    url(r'^login/$', 'apps.admin.views.login_action'),
    url(r'^logout/$', 'apps.admin.views.logout_action'),
    url(r'^login_check/$', 'apps.admin.views.login_check'),
)


