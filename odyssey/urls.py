from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'odyssey.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
