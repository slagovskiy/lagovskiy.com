from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

# from filebrowser.sites import site

from .settings import MEDIA_ROOT, MEDIA_URL
from .media.views import media
from .views import index
from .media.api import APIMediaFile, APIMediaFolder

urlpatterns = [

    url(r'^$', index, name='home'),

    url('^api/v1/media/file/', APIMediaFile.as_view(), name='api_mediafile'),
    url('^api/v1/media/folder/', APIMediaFolder.as_view(), name='api_mediafolder'),

    url(r'^blog/', include('odyssey.blog.urls')),

    url(r'^media/(?P<path>.*)$', media),

    url(r'^tinymce/', include('tinymce.urls')),

    path('pages/', include('django.contrib.flatpages.urls')),

    path('admin/', admin.site.urls),
]

# urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
