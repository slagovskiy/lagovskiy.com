from django.conf.urls import url
from .views import index
from .views import tag, category
from .views import mylinks, mylinks_all, mylinks_edit, mylinks_save


urlpatterns = [
    url(r'^$', index, name='oadmin'),

    url(r'^links/mylinks/$', mylinks, name='oadmin_mylinks'),
    url(r'^links/mylinks/all/$', mylinks_all, name='oadmin_mylinks_all'),
    url(r'^links/mylinks/save/$', mylinks_save, name='oadmin_mylinks_save'),
    url(r'^links/mylinks/(?P<id>[-\w]+)/$', mylinks_edit, name='oadmin_mylinks_edit'),

    url(r'^blog/tag/$', tag, name='oadmin_tag'),
    url(r'^blog/tag/(?P<id>[-\w]+)/$', tag, name='oadmin_tag_get'),
    url(r'^blog/tag/save/$', tag, name='oadmin_tag_save'),

    url(r'^blog/category/$', category, name='oadmin_category'),
    url(r'^blog/category/(?P<id>[-\w]+)/$', category, name='oadmin_category_get'),
    url(r'^blog/category/save/$', category, name='oadmin_category_save'),
]