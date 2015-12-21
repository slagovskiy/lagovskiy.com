from django.conf.urls import url
from .views import index
from .views import tag, tag_all


urlpatterns = [
    url(r'^$', index, name='oadmin_dashboard'),
    url(r'^tag/$', tag, name='oadmin_tag'),
    url(r'^tag/all/$', tag_all, name='oadmin_tag_all'),
]
