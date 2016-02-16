from django.conf.urls import url
from .views import index, login
from .views import tag, category
from .views import mylinks


urlpatterns = [
    url(r'^$', index, name='oadmin'),

    url(r'^login/$', login, name='login'),

    url(r'^links/mylink/$', mylinks, name='admin_mylink'),
    url(r'^links/mylink/(?P<id>[-\w]+)/$', mylinks, name='admin_mylink_get'),
    url(r'^links/mylink/save/$', mylinks, name='admin_mylink_save'),

    url(r'^blog/tag/$', tag, name='admin_tag'),
    url(r'^blog/tag/(?P<id>[-\w]+)/$', tag, name='admin_tag_get'),
    url(r'^blog/tag/save/$', tag, name='admin_tag_save'),

    url(r'^blog/category/$', category, name='admin_category'),
    url(r'^blog/category/(?P<id>[-\w]+)/$', category, name='admin_category_get'),
    url(r'^blog/category/save/$', category, name='admin_category_save'),
]
