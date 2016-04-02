from django.conf.urls import url
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from apps.blog.models import Post


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
        return reverse('blog_post', args=(item.slug,))

    def lastmod(self, item):
        return item.published
