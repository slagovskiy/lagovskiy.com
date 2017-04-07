from django.conf.urls import url
from .views import photo_view

urlpatterns = [
    url(r'^$', photo_view, name='photo'),
    #url(r'^tag/(?P<slug>[-\w]+)/$', photo_by_tag, name='photo_by_tag'),
    #url(r'^category/(?P<slug>[-\w]+)/$', photo_by_album, name='photo_by_album'),
    #url(r'^view/(?P<slug>[-\w]+)/$', photo_item_view, name='photo_item'),
]
