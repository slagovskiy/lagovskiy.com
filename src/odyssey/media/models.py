import os
import uuid

from django.db import models
from ..settings import SERVER


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


class MediaFile(models.Model):
    def mediafile_path(instance, filename):
        if instance.uid == None:
            instance.uid = str(uuid.uuid1())
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(instance.uid, ext)
        return os.path.join('mediafile', filename)
        # return os.path.join(os.path.join('mediafile', instance.uid), filename)

    uid = models.TextField(
        max_length=40,
        blank=True,
        null=True
    )

    file = models.ImageField(
        'File',
        blank=True,
        null=True,
        upload_to=mediafile_path
    )
    folder = models.ForeignKey(
        MediaFolder,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(
        'Name',
        max_length=255,
        blank=True,
        null=True
    )
    description = models.CharField(
        'Description',
        max_length=255,
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<MediaFile %s>' % self.name

    def url(self):
        return SERVER + self.file.url

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if MediaFolder.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid1())
        super(MediaFile, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name = 'Media File'
        verbose_name_plural = 'Media Files'
