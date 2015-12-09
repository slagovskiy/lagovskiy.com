from django.conf.urls import url
from django.contrib import admin
from .views import index

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^admin/', admin.site.urls),
]
