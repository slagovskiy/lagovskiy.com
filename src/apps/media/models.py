from django.db import models
from apps.userext.models import User


class Folder(models.Model):
    slug = models.SlugField(
        max_length=255
    )
    name = models.TextField(
        max_length=255
    )
    author = models.ForeignKey(
        User,
        blank=True
    )
    description = models.CharField(
        max_length=512,
        default=''
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<Folder %s>' % self.name

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Folder.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['name']
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'
