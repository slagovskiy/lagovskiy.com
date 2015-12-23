from django.conf.urls import url
from .views import index
from .views import tag, tag_all, tag_edit, tag_new, tag_save


urlpatterns = [
    url(r'^$', index, name='oadmin_dashboard'),
    url(r'^blog/tag/$', tag, name='oadmin_tag'),
    url(r'^blog/tag/all/$', tag_all, name='oadmin_tag_all'),
    url(r'^blog/tag/new/$', tag_new, name='oadmin_tag_new'),
    url(r'^blog/tag/save/$', tag_save, name='oadmin_tag_save'),
    url(r'^blog/tag/(?P<id>[-\w]+)/$', tag_edit, name='oadmin_tag_edit'),
]
