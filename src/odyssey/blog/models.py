import os
import uuid
from django.db import models

from ..userext.models import User


class Category(models.Model):
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
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
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
    def images_path(instance, filename):
        if instance.uid == None:
            instance.uid = str(uuid.uuid1())
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join('blog', instance.uid), filename)

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
        auto_now_add=True,
        editable=False,
        blank=True
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
        default=''
    )
    content = models.TextField(
        default=''
    )
    content_prev = models.TextField(
        default=''
    )
    social_image = models.ImageField(
        'Social image',
        blank=True,
        null=True,
        upload_to=images_path
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

    class Meta:
        ordering = ['-created']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    post = models.ForeignKey(Post)
    path = models.TextField(
        default=''
    )
    username = models.CharField(
        max_length=255,
        default=''
    )
    email = models.CharField(
        max_length=255,
        default=''
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        blank=True
    )
    allowed = models.BooleanField(
        default=True
    )
    content = models.TextField(
        default=''
    )
    agent = models.CharField(
        max_length=255,
        default=''
    )
    ip = models.CharField(
        max_length=15,
        default=''
    )

    def __str__(self):
        return '<Comment %s, %s, %s>' % (self.username, self.created, self.path)

    class Meta:
        ordering = ['path', ]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
