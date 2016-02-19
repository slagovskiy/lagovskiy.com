from django.conf.urls import url
from .views import index, login_action, logout_action
from .views import tag, category, post, post_tag, post_category, post_preview
from .views import mylink


urlpatterns = [
    url(r'^$', index, name='admin'),

    url(r'^login/$', login_action, name='login'),
    url(r'^logout/$', logout_action, name='logout'),

    url(r'^blog/tag/$', tag, name='admin_tag'),
    url(r'^blog/tag/(?P<id>[-\w]+)/$', tag, name='admin_tag_get'),
    url(r'^blog/tag/save/$', tag, name='admin_tag_save'),

    url(r'^blog/category/$', category, name='admin_category'),
    url(r'^blog/category/(?P<id>[-\w]+)/$', category, name='admin_category_get'),
    url(r'^blog/category/save/$', category, name='admin_category_save'),

    url(r'^blog/post/$', post, name='admin_post'),
    url(r'^blog/post/tag/$', post_tag, name='admin_post_tag_get'),
    url(r'^blog/post/category/$', post_category, name='admin_post_category_get'),
    url(r'^blog/post/preview/$', post_preview, name='admin_post_preview'),
    url(r'^blog/post/(?P<id>[-\w]+)/$', post, name='admin_post_get'),
    url(r'^blog/post/save/$', post, name='admin_post_save'),

    url(r'^links/mylink/$', mylink, name='admin_mylink'),
    url(r'^links/mylink/(?P<id>[-\w]+)/$', mylink, name='admin_mylink_get'),
    url(r'^links/mylink/save/$', mylink, name='admin_mylink_save'),
]
