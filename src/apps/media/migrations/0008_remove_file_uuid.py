# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 05:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0007_auto_20160425_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='uuid',
        ),
    ]
