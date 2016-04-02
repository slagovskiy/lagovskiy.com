from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from .views import index
from toolbox.sitemap import BlogSitemap

sitemaps = {
    'pages': BlogSitemap()
}


urlpatterns = [
    url(r'^$', index, name='home'),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),

    url(r'^blog/', include('apps.blog.urls')),
    url(r'^media/', include('apps.media.urls')),
    url(r'^admin/', include('apps.admin.urls')),
    url(r'^djadmin/', admin.site.urls, name='djadmin'),
]
