from django.contrib.sitemaps import Sitemap
from apps.blog.models import *
from settings_local import DOMAIN_NAME

class BlogSitemap(Sitemap):
    # always
    # hourly
    # daily
    # weekly
    # monthly
    # yearly
    # never
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.all().filter(status=Post.PUBLISHED_STATUS).order_by('-published')

    def location(self, item):
        return DOMAIN_NAME + item.get_absolute_url()

    def lastmod(self, item):
        return item.published

