# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0005_auto_20170420_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='devices',
            field=models.ManyToManyField(blank=True, to='photo.Device'),
        ),
    ]
