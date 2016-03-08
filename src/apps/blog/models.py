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

    def get_absolute_url(self):
        return '/blog/category/%s/' % self.slug

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

    def get_absolute_url(self):
        return '/blog/tag/%s/' % self.slug

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

    def __str__(self):
        return '<Post %s>' % self.title

    def get_absolute_url(self):
        return '/blog/view/%s/' % self.slug

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
