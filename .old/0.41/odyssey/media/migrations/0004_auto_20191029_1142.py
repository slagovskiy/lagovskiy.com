# Generated by Django 2.2.6 on 2019-10-29 04:42

from django.db import migrations, models
import odyssey.media.models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_mediafile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=odyssey.media.models.MediaFile.mediafile_path, verbose_name='File'),
        ),
    ]
