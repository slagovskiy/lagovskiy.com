import os
import uuid

from django.db import models

from ..userext.models import User
from ..media.models import MediaFile


class Link(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    link = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    icon = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    deleted = models.BooleanField(
        default=False
    )


    def __str__(self):
        return '<Link %s>' % self.name


    class Meta:
        ordering = ['name',]
        verbose_name = 'Link'
        verbose_name_plural = 'Links'