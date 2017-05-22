import os
import uuid
from django.db import models
from django.urls import reverse
from ..userext.models import User
from ..staticstic.models import visitor_count
from ..settings import SITE_URL


class Album(models.Model):
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        max_length=255,
        default=''
    )
    order = models.IntegerField(
        default=10
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<Album %s>' % self.name

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Album.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


class Tag(models.Model):
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        max_length=255,
        default=''
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<Tag %s>' % self.name

    def photos_count(self):
        return self.photo_set.all().filter(status=Photo.PUBLISHED_STATUS).count()

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Tag.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class DeviceType(models.Model):
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        max_length=255,
        default=''
    )
    show_in_menu = models.BooleanField(
        default=True
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<DeviceType %s>' % self.name

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if DeviceType.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['name',]
        verbose_name = 'Device type'
        verbose_name_plural = 'Device types'


class Device(models.Model):
    def image_path(instance, filename):
        if instance.uid == None:
            instance.uid = str(uuid.uuid1())
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join('device', instance.uid), filename)

    uid = models.TextField(
        max_length=40,
        blank=True,
        null=True
    )
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        max_length=255,
        default=''
    )
    device_type = models.ForeignKey(
        'DeviceType'
    )
    deleted = models.BooleanField(
        default=False
    )
    image = models.ImageField(
        'Image',
        default='',
        upload_to=image_path
    )
    content = models.TextField(
        default=''
    )

    def __str__(self):
        return '<Device %s>' % self.name

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Device.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    def image_preview(self):
        if self.image:
            return '<img src="%s?w=300" border="0"/>' % self.image.url
        else:
            return ''

    image_preview.short_description = 'Image preview'
    image_preview.allow_tags = True

    def image_admin_preview(self):
        if self.image:
            preview = '<img src="%s?h=24" border="0"/>' % self.image.url
            return preview
        else:
            return ''

    image_admin_preview.short_description = 'Image'
    image_admin_preview.allow_tags = True

    def visitor_count(self):
        return visitor_count(reverse('photo_item', args=[self.slug]))

    class Meta:
        ordering = ['name',]
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'


class Photo(models.Model):
    def image_path(instance, filename):
        if instance.uid == None:
            instance.uid = str(uuid.uuid1())
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join('photo', instance.uid), filename)

    DRAFT_STATUS = 0
    HIDDEN_STATUS = 1
    PUBLISHED_STATUS = 2

    STATUS_CHOICES = (
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
        (PUBLISHED_STATUS, 'Public'),
    )

    uid = models.TextField(
        max_length=40,
        blank=True,
        null=True
    )
    slug = models.SlugField(
        max_length=255,
        unique=True
    )
    title = models.TextField(
        max_length=255,
        blank=True
    )
    author = models.ForeignKey(
        User,
        blank=True
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=DRAFT_STATUS
    )
    sticked = models.BooleanField(
        default=False
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True
    )
    published = models.DateTimeField(
        blank=True,
        null=True
    )
    albums = models.ManyToManyField(
        Album,
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True
    )
    image = models.ImageField(
        'Image',
        default='',
        upload_to=image_path
    )
    devices = models.ManyToManyField(
        Device,
        blank=True
    )

    def __str__(self):
        return '<Image %s>' % self.title

    def image_preview(self):
        if self.image:
            return '<img src="%s?w=300" border="0"/>' % self.image.url
        else:
            return ''

    image_preview.short_description = 'Image preview'
    image_preview.allow_tags = True

    def image_admin_preview(self):
        if self.image:
            preview = '<img src="%s?s=24" border="0"/>' % self.image.url
            return preview
        else:
            return ''

    image_admin_preview.short_description = 'Image'
    image_admin_preview.allow_tags = True

    def get_photo_url(self):
        path = SITE_URL + self.image.url
        return path

    def get_post_url(self):
        path = SITE_URL + reverse('photo_item_view', args=[self.slug])
        return path


    def visitor_count(self):
        return visitor_count(self.image.url)


    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Photo.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['-created']
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
