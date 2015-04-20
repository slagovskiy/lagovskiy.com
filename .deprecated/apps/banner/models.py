from django.db import models

class Banner(models.Model):
    slug = models.SlugField(max_length=255, verbose_name=u'Key', unique=True,)
    name = models.CharField(max_length=255, verbose_name=u'Name',)
    code = models.TextField(default='', verbose_name=u'Code')
    sort = models.IntegerField(default=10, verbose_name=u'Sort')
    hidden = models.BooleanField(default=False, verbose_name=u'Hidden')
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted')

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return '/banner/' + self.slug + '/'

    class Meta:
        ordering = ['sort']
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
