from django.conf.urls import url
from .views import media_file


urlpatterns = [
    url(r'^file/(?P<key>[-\w]+)/$', media_file, name='media_file'),
    url(r'^files/(?P<y>[-\w]+)/(?P<m>[-\w]+)/(?P<d>[-\w]+)/(?P<key>[-\w]+)/$', media_file, name='media_file'),
    url(r'^file/(?P<key>[-\w]+)/(?P<filename>[-\w\.]+)$', media_file, name='media_file'),
    url(r'^files/(?P<y>[-\w]+)/(?P<m>[-\w]+)/(?P<d>[-\w]+)/(?P<key>[-\w]+)/(?P<filename>[-\w\.]+)$', media_file, name='media_file'),
]
