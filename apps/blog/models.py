from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from mptt.models import MPTTModel

from apps.statistic.models import visitor_count

from settings import *
from settings_local import *

class Category(models.Model):
    slug = models.SlugField(max_length=255, verbose_name=u'Key', unique=True,)
    name = models.CharField(max_length=255, verbose_name=u'Name',)
    sort = models.IntegerField(default=10, verbose_name=u'Sort')
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted')

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return '/blog/category/' + self.slug + '/'

    def post_count(self):
        return self.post_set.all().filter(status=2).count()

    class Meta:
        ordering = ['sort']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    slug = models.SlugField(max_length=255, verbose_name=u'Key', unique=True,)
    name = models.CharField(max_length=255, verbose_name=u'Name',)
    sort = models.IntegerField(default=10, verbose_name=u'Sort')
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted')

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return '/blog/tag/' + self.slug + '/'

    def post_count(self):
        return self.post_set.all().filter(status=2).count()

    class Meta:
        ordering = ['sort']
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

    slug = models.SlugField(max_length=255, verbose_name=u'Key',)
    title = models.TextField(max_length=255, verbose_name=u'Title',)
    author = models.ForeignKey(User, blank=True, null=True,)
    published_revision = models.IntegerField(default=0, verbose_name=u'Published revision',)
    description = models.CharField(max_length=512, default='', verbose_name=u'Description for META',)
    keywords = models.CharField(max_length=512, default='', verbose_name=u'Keywords for META',)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name=u'Status',)
    sticked = models.BooleanField(default=False, verbose_name=u'Sticked',)
    comments_enabled = models.BooleanField(default=True, verbose_name=u'Allow comments',)
    comments_moderated = models.BooleanField(default=True, verbose_name=u'Moderated comments')
    do_ping = models.BooleanField(default=False, verbose_name=u'do ping',)
    published = models.DateTimeField(blank=True, null=True, verbose_name=u'Published',)
    categories = models.ManyToManyField(Category, blank=True, verbose_name=u'Categories',)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'Tags',)

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return '/blog/view/' + self.slug + '/'

    def get_comment_save_url(self):
        return '/blog/comment/save/' + str(self.id) + '/'

    def teaser(self):
        if self.published_revision > 0:
            return PostRevision.objects.filter(
                post=self, revision=self.published_revision)[0].teaser
        else:
            return 'no revision'

    def content(self):
        if self.published_revision > 0:
            return PostRevision.objects.filter(
                post=self, revision=self.published_revision)[0].content
        else:
            return 'no revision'

    def comment_count(self):
        return self.comment_set.all().exclude(allowed=False).exclude(deleted=True).count()

    def visitor_count(self):
        return visitor_count(self.get_absolute_url())

    def comments(self):
        return self.comment_set.all()

    class Meta:
        ordering = ['status', 'slug']

class PostRevision(models.Model):
    post = models.ForeignKey(Post)
    revision = models.IntegerField(default=1, verbose_name=u'Version of post',)
    teaser = models.TextField(default='', verbose_name=u'Teaser')
    content = models.TextField(default='', verbose_name=u'Content',)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Created',)

    def __unicode__(self):
        return u'%s %s' % (self.post.slug, self.revision)

    def last_revision(self):
        mx = PostRevision.objects.filter(
            post=self.post).aggregate(Max('revision'))['revision__max']
        if mx == -1:
            mx = 0
        return mx

    class Meta:
        ordering = ['created']

class Comment(MPTTModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u'User',)
    name = models.CharField(max_length=50, default='', verbose_name=u'Name for anonymous',)
    email = models.CharField(max_length=50, default='', verbose_name=u'Email for anonymous', blank=True,)
    web = models.CharField(max_length=255, default='', verbose_name=u'Web site', blank=True,)
    content = models.TextField(verbose_name=u'Content',)
    published = models.DateTimeField(auto_now_add=True, verbose_name=u'Published',)
    allowed = models.BooleanField(default=False, verbose_name=u'Allowed',)
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted',)
    agent = models.CharField(max_length=255, default='', verbose_name=u'User agent',)
    ip = models.CharField(max_length=15, default='', verbose_name=u'IP',)

    def __unicode__(self):
        return u'%s %s' % (self.post.slug, self.published)

    def get_absolute_url(self):
        return '/blog/post/' + self.post.slug + '/#' + str(self.id)

    class Meta:
        ordering = ['tree_id', 'lft']

class SubscribePost(models.Model):
    post = models.ForeignKey(Post)
    email = models.CharField(max_length=255, default='', verbose_name=u'Email',)
    active = models.BooleanField(default=True, verbose_name=u'Active subscribe',)

class CommentMessageQueue(models.Model):
    subscribe = models.ForeignKey(SubscribePost)
    comment = models.ForeignKey(Comment)
    added = models.DateTimeField(auto_now_add=True,)
    sended = models.DateTimeField(null=True, blank=True,)
    active = models.BooleanField(default=False,)

class PostImage(models.Model):
    post = models.ForeignKey(Post)
    description = models.CharField(max_length=255, default='', verbose_name=u'Description')
    img_xxs = models.CharField(max_length=255, default='', verbose_name=u'XXS')
    img_xs = models.CharField(max_length=255, default='', verbose_name=u'XS')
    img_s = models.CharField(max_length=255, default='', verbose_name=u'S')
    img_m = models.CharField(max_length=255, default='', verbose_name=u'M')
    img_l = models.CharField(max_length=255, default='', verbose_name=u'L')
    img_xl = models.CharField(max_length=255, default='', verbose_name=u'XL')
    img_xxl = models.CharField(max_length=255, default='', verbose_name=u'XXL')
    img_xxxl = models.CharField(max_length=255, default='', verbose_name=u'XXXL')
    img_orig = models.CharField(max_length=255, default='', verbose_name=u'ORIG')

    def __unicode__(self):
        return self.img_l

    def get_absolute_url(self):
        return self.img_l

    class Meta:
        pass

