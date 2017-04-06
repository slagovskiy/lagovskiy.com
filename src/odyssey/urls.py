from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView

from .toolbox.sitemap import BlogSitemap
from .views import index, captcha, captcha_check
from .media.views import media


sitemaps = {
    'pages': BlogSitemap()
}


urlpatterns = [
    url(r'^$', index, name='home'),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),

    url(r'^captcha/$', captcha, name='captcha'),
    url(r'^captcha_check/(?P<code>[-\w]+)/$', captcha_check, name='captcha_check'),

    url(r'^blog/', include('odyssey.blog.urls')),

    url(r'^media/(?P<path>.*)$', media),

    url(r'^admin/', admin.site.urls, name='admin'),
]
