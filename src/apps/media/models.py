import os
from uuid import uuid4
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import format_html

from apps.userext.models import User
from toolbox.imghdr import what
from .utils import create_icon


class File(models.Model):
    def upload_to(self, filename):
        dy = str(datetime.now().year)
        dm = str(datetime.now().month)
        if len(dm) == 1:
            dm = '0' + dm
        dd = str(datetime.now().day)
        if len(dd) == 1:
            dd = '0' + dd
        if self.uuid is None:
            self.uuid = str(uuid4())
        path = os.path.join(
            os.path.join(
                os.path.join(
                    os.path.join(
                        os.path.join('files', dy), dm), dd), self.uuid), filename)
        return path

    name = models.CharField(
        max_length=255
    )
    uuid = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
    f = models.FileField(
        upload_to=upload_to,
        null=True,
        verbose_name='File'
    )
    is_image = models.BooleanField(
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

    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = str(uuid4())
        super(File, self).save(*args, **kwargs)
        if what(self.f.path):
            self.is_image = True
        else:
            self.is_image = False
            create_icon(self.f.path)

    def preview(self):
        if self.uuid:
            return format_html('<img src="%s?s=60">' % reverse('media_file', args=(self.uuid,)))
        else:
            return ''

    class Meta:
        ordering = ['name']
        verbose_name = 'File'
        verbose_name_plural = 'Files'
