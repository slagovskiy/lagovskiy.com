from django.db import models


class MediaFolder(models.Model):
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    deleted = models.BooleanField(
        default=False
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return '<MediaFolder %s>' % self.name

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if MediaFolder.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['name']
        verbose_name = 'Media folder'
        verbose_name_plural = 'Media folders'
