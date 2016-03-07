from django.db import models
from apps.userext.models import User


class Folder(models.Model):
    uuid = models.CharField(
        max_length=255,
        default=''
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
    added = models.DateTimeField(
        auto_now_add=True
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<Folder %s>' % self.name

    @staticmethod
    def exist(name=None, author=None):
        if name is None:
            return False
        elif author is None:
            return False
        else:
            if Folder.objects.filter(name=name, author=author).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['name']
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'


class File(models.Model):
    uuid = models.CharField(
        max_length=255,
        default=''
    )
    name = models.CharField(
        max_length=255
    )
    folder = models.ForeignKey(
        Folder,
        blank=True
    )
    image = models.BooleanField(
        default=False
    )
    author = models.ForeignKey(
        User,
        blank=True
    )
    added = models.DateTimeField(
        auto_now_add=True
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<File %s>' % self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'File'
        verbose_name_plural = 'Files'
