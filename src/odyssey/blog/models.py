import os
import uuid

from django.db import models

from ..userext.models import User
from ..media.models import MediaFile


class Category(models.Model):
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    order = models.IntegerField(
        default=10
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<Category %s>' % self.name

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Category.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '<Tag %s>' % self.name

    def post_count(self):
        return self.post_set.all().filter(status=Post.PUBLISHED_STATUS).count()

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


class Post(models.Model):
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
        max_length=255
    )
    title = models.TextField(
        max_length=255
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )
    description = models.CharField(
        max_length=512,
        blank=True,
        default=''
    )
    keywords = models.CharField(
        max_length=512,
        blank=True,
        default=''
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=DRAFT_STATUS
    )
    sticked = models.BooleanField(
        default=False
    )
    comments_enabled = models.BooleanField(
        default=True
    )
    comments_moderated = models.BooleanField(
        default=True
    )
    do_ping = models.BooleanField(
        default=False
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    published = models.DateTimeField(
        blank=True,
        null=True
    )
    categories = models.ManyToManyField(
        Category,
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True
    )
    teaser = models.TextField(
        blank=True,
        default=''
    )
    content = models.TextField(
        blank=True,
        default=''
    )
    social_image = models.ForeignKey(
        MediaFile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '<Post %s>' % self.title

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Post.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid1())
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
