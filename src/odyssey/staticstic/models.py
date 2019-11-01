from django.db import models
from django.db.models import Count
import logging


class Visitor(models.Model):
    point = models.CharField(
        max_length=255,
        default=''
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True
    )
    ip_address = models.CharField(
        max_length=15,
        default='',
        null=True,
        blank=True
    )
    user_agent = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )
    referer = models.CharField(
        max_length=255,
        default='',
        null=True,
        blank=True
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    browser_family = models.CharField(
        max_length=50,
        default='',
        null=True,
        blank=True
    )
    browser_version = models.CharField(
        max_length=10,
        default='',
        null=True,
        blank=True
    )
    os_family = models.CharField(
        max_length=50,
        default='',
        null=True,
        blank=True
    )
    os_version = models.CharField(
        max_length=10,
        default='',
        null=True,
        blank=True
    )
    device_family = models.CharField(
        max_length=50,
        default='',
        null=True,
        blank=True
    )
    is_mobile = models.BooleanField(
        default=False
    )
    is_tablet = models.BooleanField(
        default=False
    )
    is_touch_capable = models.BooleanField(
        default=False
    )
    is_pc = models.BooleanField(
        default=False
    )
    is_bot = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '%s %s %s' %(self.date, self.point, self.user_agent)

    class Meta:
        ordering = ['date']


def visitor_count(point):
    c = 0
    try:
        c = Visitor.objects.filter(point=point).aggregate(Count('id'))['id__count']
    except:
        logging.exception('Error get count of visitors')
    return c
