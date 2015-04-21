# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('deleted', models.BooleanField(verbose_name='Deleted', default=False)),
                ('name', models.TextField(max_length=255, verbose_name='Name')),
                ('sort', models.IntegerField(verbose_name='Sort', default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('deleted', models.BooleanField(verbose_name='Deleted', default=False)),
                ('name', models.TextField(max_length=255, verbose_name='Name')),
                ('sort', models.IntegerField(verbose_name='Sort', default=10)),
            ],
        ),
    ]
