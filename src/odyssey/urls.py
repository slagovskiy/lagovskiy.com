from django.conf.urls import include, url
from django.contrib import admin
from .views import index


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^blog/', include('apps.blog.urls')),
    url(r'^media/', include('apps.media.urls')),
    url(r'^admin/', include('apps.admin.urls')),
    url(r'^djadmin/', admin.site.urls, name='djadmin'),
]
