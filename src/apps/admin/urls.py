from django.conf.urls import url
from .views import index, login_action, logout_action
from .views import global_view
from .views import tag, category, post, post_tag, post_category, post_preview
from .views import mylink
from .views import media_folder, upload, media_files, media_file


urlpatterns = [
    url(r'^$', index, name='admin'),

    url(r'^login/$', login_action, name='login'),
    url(r'^logout/$', logout_action, name='logout'),

    url(r'^blog/global/$', global_view, name='admin_global'),
    url(r'^blog/global/(?P<id>[-\w]+)/$', global_view, name='admin_global_get'),
    url(r'^blog/global/save/$', global_view, name='admin_global_save'),

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

    url(r'^media/upload/$', upload, name='admin_upload'),
    url(r'^media/files/$', media_files, name='admin_files'),
    url(r'^media/files/(?P<id>[-\w]+)/$', media_files, name='admin_files'),
    url(r'^media/file/$', media_file, name='admin_file'),
    url(r'^media/file/(?P<id>[-\w]+)/$', media_file, name='admin_file_get'),
    url(r'^media/file/<save>/$', media_file, name='admin_file_save'),
    url(r'^media/folder/$', media_folder, name='admin_folder'),
    url(r'^media/folder/(?P<id>[-\w]+)/$', media_folder, name='admin_folder_get'),
    url(r'^media/folder/save/$', media_folder, name='admin_folder_save'),
]
