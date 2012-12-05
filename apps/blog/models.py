from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from mptt.models import MPTTModel


class Category(models.Model):
    slug = models.SlugField(max_length=255, verbose_name=u'Key', unique=True,)
    name = models.CharField(max_length=255, verbose_name=u'Name',)
    sort = models.IntegerField(default=10, verbose_name=u'Sort')
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted')

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return '/blog/category/' + self.slug + '/'

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
        return '/blog/post/' + self.slug + '/'


    def excerpt(self):
        if self.published_revision > 0:
            return PostRevision.objects.filter(
                post=self, revision=self.published_revision)[0].excerpt
        else:
            return 'no revision'

    def content(self):
        if self.published_revision > 0:
            return PostRevision.objects.filter(
                post=self, revision=self.published_revision)[0].content
        else:
            return 'no revision'

    def comment_count(self):
        return self.comment_set.all().exclude(allowed=False).count()

    class Meta:
        ordering = ['status', 'slug']

class PostRevision(models.Model):
    post = models.ForeignKey(Post)
    revision = models.IntegerField(default=1, verbose_name=u'Version of post',)
    excerpt = models.TextField(default='', verbose_name=u'Excerpt')
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
    email = models.CharField(max_length=50, default='', verbose_name=u'Email for anonymous',)
    web = models.CharField(max_length=255, default='', verbose_name=u'Web site',)
    content = models.TextField(verbose_name=u'Content',)
    published = models.DateTimeField(auto_now_add=True, verbose_name=u'Published',)
    allowed = models.BooleanField(default=False, verbose_name=u'Allowed',)
    deleted = models.BooleanField(default=False, verbose_name=u'Deleted',)
    agent = models.CharField(max_length=255, default='', verbose_name=u'User agent',)
    ip = models.CharField(max_length=15, default='', verbose_name=u'IP',)

    def __unicode__(self):
        return u'%s %s' % (self.post.slug, self.published)

    def get_absolute_url(self):
        return '/blog/post/' + self.post.slug + '/#' + self.id

    class Meta:
        ordering = ['tree_id', 'lft']
