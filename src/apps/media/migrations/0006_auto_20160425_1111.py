# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 05:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0005_file_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='author',
        ),
        migrations.RemoveField(
            model_name='file',
            name='folder',
        ),
        migrations.DeleteModel(
            name='Folder',
        ),
    ]