from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel


class Category(models.Model):
    slug = models.SlugField(max_length=255, verbose_name=u'Key', unique=True,)
    name = models.CharField(max_length=255, verbose_name=u'Name',)
    sort = models.IntegerField(default=10, verbose_name=u'Sort')
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted')

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return '/blog/category/' + self.slug + '/'

    class Meta:
        ordering = ['sort']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
