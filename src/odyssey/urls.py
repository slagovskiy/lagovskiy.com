from django.conf.urls import include, url
from django.contrib import admin
from .views import index


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^admin/', include('apps.admin.urls')),
    url(r'^djadmin/', admin.site.urls, name='djadmin'),
]
