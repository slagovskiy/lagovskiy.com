from django.conf.urls import include, url
from django.contrib import admin
from .views import index


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^oadmin/', include('apps.oadmin.urls')),
    url(r'^admin/', admin.site.urls),
]
