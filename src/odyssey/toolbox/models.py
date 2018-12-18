from django.db import models
from ..blog.models import Post


class Global(models.Model):
    slug = models.SlugField(
        unique=True
    )
    value = models.CharField(
        max_length=255,
        default=''
    )

    def __str__(self):
        return '<Global %s>' % self.slug

    @staticmethod
    def get(slug=None):
        if slug is None:
            return None
        else:
            g = Global.objects.filter(slug=slug).first()
            if g is None:
                return ''
            else:
                return g.value

    @staticmethod
    def set(slug=None, value=''):
        if slug is None:
            return False
        else:
            g = Global.objects.filter(slug=slug).first()
            if g is None:
                g = Global.objects.create(
                    slug=slug,
                    value=value
                )
                g.save()
                return True
            else:
                g.value = value
                g.save()
                return True

    class Meta:
        ordering = ['slug']
        verbose_name = 'Global'
        verbose_name_plural = 'Globals'


class PingServer(models.Model):
    address = models.CharField(
        max_length=255,
        verbose_name=u'Address',
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Deleted',
    )

    def __str__(self):
        return self.address

    class Meta:
        ordering = ['address']

class PingResult(models.Model):
    date = models.DateTimeField(
        auto_now_add=True
    )
    pingserver = models.ForeignKey(
        PingServer,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    passed = models.BooleanField(
        default=False
    )
    message = models.CharField(
        max_length=255,
        default=''
    )

    def __unicode__(self):
        return '%s %s' %(self.date, str(self.passed))
