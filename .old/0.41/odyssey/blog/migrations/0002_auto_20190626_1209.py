# Generated by Django 2.2.2 on 2019-06-26 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
