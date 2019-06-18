# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-15 09:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import odyssey.blog.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20161222_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.TextField(blank=True, max_length=40, null=True)),
                ('description', models.CharField(default='', max_length=512)),
                ('media_file', models.FileField(blank=True, null=True, upload_to=odyssey.blog.models.Media.media_path, verbose_name='Media file')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]