from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from .settings import MEDIA_ROOT, MEDIA_URL

from .media.views import media

from .views import index

urlpatterns = [

    url(r'^$', index, name='home'),

    url(r'^blog/', include('odyssey.blog.urls')),

    url(r'^media/(?P<path>.*)$', media),

    url(r'^tinymce/', include('tinymce.urls')),

    path('pages/', include('django.contrib.flatpages.urls')),

    path('admin/', admin.site.urls),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
