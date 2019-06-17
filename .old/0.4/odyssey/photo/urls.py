from django.conf.urls import url
from django.views.generic import RedirectView

from .views import photo_view, photo_by_album, photo_by_tag, photo_item_view, devices_view, device_view

urlpatterns = [
    url(r'^$', photo_view, name='photo'),
    url(r'^tag/(?P<slug>[-\w]+)/$', photo_by_tag, name='photo_by_tag'),
    url(r'^tag/$', RedirectView.as_view(pattern_name='photo'), name='photo_by_tag_index'),
    url(r'^album/(?P<slug>[-\w]+)/$', photo_by_album, name='photo_by_album'),
    url(r'^album/$', RedirectView.as_view(pattern_name='photo'), name='photo_by_album_index'),
    url(r'^view/(?P<slug>[-\w]+)/$', photo_item_view, name='photo_item_view'),
    url(r'^view/$', RedirectView.as_view(pattern_name='photo'), name='photo_item_view_index'),
    url(r'^devices/(?P<slug>[-\w]+)/$', devices_view, name='devices_by_type'),
    url(r'^devices/$', RedirectView.as_view(pattern_name='photo'), name='devices_by_type_index'),
    url(r'^device/(?P<slug>[-\w]+)/$', device_view, name='device_view'),
    url(r'^device/$', RedirectView.as_view(pattern_name='photo'), name='device_index'),
]
