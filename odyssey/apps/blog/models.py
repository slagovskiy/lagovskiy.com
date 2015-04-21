from django.db import models


class Category(models.Model):
    slug = models.SlugField(unique=True, max_length=255, verbose_name=u'Slug')
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted')
    name = models.TextField(max_length=255, verbose_name=u'Name')
    sort = models.IntegerField(default=10, verbose_name=u'Sort')

    def __str__(self):
        return '[%s] %s' % (self.sort, self.name)

    def get_absolute_url(self):
        return '/blog/category/%s/' % self.slug


class Tag(models.Model):
    slug = models.SlugField(unique=True, max_length=255, verbose_name=u'Slug')
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted')
    name = models.TextField(max_length=255, verbose_name=u'Name')
    sort = models.IntegerField(default=10, verbose_name=u'Sort')

    def __str__(self):
        return '[%s] %s' % (self.sort, self.name)

    def get_absolute_url(self):
        return '/blog/category/%s/' % self.slug
