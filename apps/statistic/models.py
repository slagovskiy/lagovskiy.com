from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count

import logging

class Visitor(models.Model):
    point = models.CharField(max_length=255, default='', verbose_name=u'Point',)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True, verbose_name='Session id',)
    ip_address = models.CharField(max_length=15, default='', null=True, blank=True, verbose_name=u'IP',)
    user_agent = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name=u'User agent',)
    referer = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name=u'Referer',)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u'User',)
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Published',)
    browser_family = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name=u'Browser family',)
    browser_version = models.CharField(max_length=10, default='', null=True, blank=True, verbose_name=u'Browser version',)
    os_family = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name=u'OS family',)
    os_version = models.CharField(max_length=10, default='', null=True, blank=True, verbose_name=u'OS version',)
    device_family = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name=u'Devise family',)
    is_mobile = models.BooleanField(default=False, verbose_name=u'is_mobile',)
    is_tablet = models.BooleanField(default=False, verbose_name=u'is_tablet',)
    is_touch_capable = models.BooleanField(default=False, verbose_name=u'is_touch_capable',)
    is_pc = models.BooleanField(default=False, verbose_name=u'is_pc',)
    is_bot = models.BooleanField(default=False, verbose_name=u'is_bot',)

    def __unicode__(self):
        return "%s %s", (self.date, self.point)

    class Meta:
        ordering = ['date']

def visitor_count(point):
    c = 0
    try:
        c = Visitor.objects.filter(point=point).aggregate(Count('id'))['id__count']
    except:
        logging.exception('Error get count of visitors')
    return c