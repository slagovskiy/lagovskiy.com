# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160220_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Hidden'), (2, 'Public')], default=0),
        ),
    ]