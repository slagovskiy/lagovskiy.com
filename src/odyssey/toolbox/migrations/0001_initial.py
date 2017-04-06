# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Global',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('value', models.CharField(default='', max_length=255)),
            ],
            options={
                'ordering': ['slug'],
                'verbose_name': 'Global',
                'verbose_name_plural': 'Globals',
            },
        ),
    ]