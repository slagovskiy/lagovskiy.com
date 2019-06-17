from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from ..blog.models import Post


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
        pass
        return Post.objects.all().filter(status=Post.PUBLISHED_STATUS).order_by('-published')

    def location(self, item):
        return reverse('blog_post', args=(item.slug,))

    def lastmod(self, item):
        return item.published
