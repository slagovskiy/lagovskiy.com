from django.conf.urls import url
from .views import index
from .views import tag, category
from .views import mylinks


urlpatterns = [
    url(r'^$', index, name='oadmin'),

    url(r'^links/mylink/$', mylinks, name='oadmin_mylink'),
    url(r'^links/mylink/(?P<id>[-\w]+)/$', mylinks, name='oadmin_mylink_get'),
    url(r'^links/mylink/save/$', mylinks, name='oadmin_mylink_save'),

    url(r'^blog/tag/$', tag, name='oadmin_tag'),
    url(r'^blog/tag/(?P<id>[-\w]+)/$', tag, name='oadmin_tag_get'),
    url(r'^blog/tag/save/$', tag, name='oadmin_tag_save'),

    url(r'^blog/category/$', category, name='oadmin_category'),
    url(r'^blog/category/(?P<id>[-\w]+)/$', category, name='oadmin_category_get'),
    url(r'^blog/category/save/$', category, name='oadmin_category_save'),
]
