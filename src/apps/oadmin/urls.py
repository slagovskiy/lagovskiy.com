from django.conf.urls import url
from .views import index
from .views import tag, tag_all, tag_edit, tag_save
from .views import category, category_all, category_edit, category_save


urlpatterns = [
    url(r'^$', index, name='oadmin_dashboard'),

    url(r'^blog/tag/$', tag, name='oadmin_tag'),
    url(r'^blog/tag/all/$', tag_all, name='oadmin_tag_all'),
    url(r'^blog/tag/save/$', tag_save, name='oadmin_tag_save'),
    url(r'^blog/tag/(?P<id>[-\w]+)/$', tag_edit, name='oadmin_tag_edit'),

    url(r'^blog/category/$', category, name='oadmin_category'),
    url(r'^blog/category/all/$', category_all, name='oadmin_category_all'),
    url(r'^blog/category/save/$', category_save, name='oadmin_category_save'),
    url(r'^blog/category/(?P<id>[-\w]+)/$', category_edit, name='oadmin_category_edit'),
]
