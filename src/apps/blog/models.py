from django.db import models
from apps.userext.models import User


class Category(models.Model):
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
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


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
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Post(models.Model):
    DRAFT_STATUS = 1
    PUBLISHED_STATUS = 2
    HIDDEN_STATUS = 3

    STATUS_CHOICES = (
        (DRAFT_STATUS, 'Draft'),
        (PUBLISHED_STATUS, 'Public'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    slug = models.SlugField(
        max_length=255
    )
    title = models.TextField(
        max_length=255
    )
    author = models.ForeignKey(
        User,
        blank=True
    )
    description = models.CharField(
        max_length=512,
        default=''
    )
    keywords = models.CharField(
        max_length=512,
        default=''
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
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
