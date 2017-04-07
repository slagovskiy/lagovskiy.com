# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-07 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import odyssey.photo.models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_auto_20170407_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(default='', upload_to=odyssey.photo.models.Photo.image_path, verbose_name='Image'),
        ),
    ]
