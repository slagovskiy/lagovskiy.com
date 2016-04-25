from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView
from .views import index, captcha, captcha_check
from toolbox.sitemap import BlogSitemap


sitemaps = {
    'pages': BlogSitemap()
}


urlpatterns = [
    url(r'^$', index, name='home'),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

    url(r'^captcha/$', captcha, name='captcha'),
    url(r'^captcha_check/(?P<code>[-\w]+)/$', captcha_check, name='captcha_check'),

    url(r'^blog/', include('apps.blog.urls')),
    url(r'^media/', include('apps.media.urls')),
    #url(r'^admin/', include('apps.admin.urls')),
    url(r'^admin/', admin.site.urls, name='admin'),
]
