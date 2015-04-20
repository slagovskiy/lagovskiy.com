# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

access_key = {
    1: 'admin',
    #2: '-',
    #4: '-',
    #8: '-',
    #16: '-',
    #32: '-',
    #64: '-',
    #128: '-',
    #256: '-',
    #512: '-',
    #1024: '-',
    #2048: '-',
    #4096: '-',
    #8192: '-',
    #16384: '-',
    #32768: '-',
    #65536: '-',
    #131072: '-',
    #262144: '-',
    #524288: '-',
    #1048576: '-',
    #2097152: '-',
    #4194304: '-',
    #8388608: '-',
    #16777216: '-',
    #33554432: '-',
    #67108864: '-',
    #134217728: '-',
    #268435456: '-',
    #536870912: '-',
}

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    access = models.BigIntegerField(default=0, verbose_name=u'Access',)

    def canAdmin(self):
        return ((self.access&1)==1)

    def canCommentAllow(self):
        return ((self.access&1)==1)

    def canCommentDelete(self):
        return ((self.access&1)==1)

def create_profile(sender, **kwargs):
    user = kwargs['instance']
    if kwargs["created"]:
        profile = UserProfile(user=user)
        profile.save()

post_save.connect(create_profile, sender=User)