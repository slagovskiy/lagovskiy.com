from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from odyssey.settings import base

urlpatterns = [
    url(r'^$', 'odyssey.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

# urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)