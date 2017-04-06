import os
import uuid
from django.db import models
from django.urls import reverse
from ..settings import STATIC_URL

from ..userext.models import User
from ..staticstic.models import visitor_count
from ..settings import SITE_URL


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
    social_image = models.ImageField(
        'Social image',
        blank=True,
        null=True,
        upload_to=images_path
    )

    def __str__(self):
        return '<Post %s>' % self.title

    def get_social_image_url(self):
        if self.social_image:
            path = SITE_URL + self.social_image.url
            return path
        else:
            return ''

    def get_post_url(self):
        path = SITE_URL + reverse('blog_post', args=[self.slug])
        return path

    def social_image_preview(self):
        if self.social_image:
            return '<img src="%s?h=100" border="0"/>' % self.social_image.url
        else:
            return ''

    social_image_preview.short_description = 'Social image preview'
    social_image_preview.allow_tags = True

    def visitor_count(self):
        return visitor_count(reverse('blog_post', args=[self.slug]))


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

    def content100(self):
        more = ''
        if len(self.content) > 100:
            more = '...'
        return self.content[:100] + more

    def post100(self):
        return self.post.title[:100]

    content100.short_description = 'Content preview'
    post100.short_description = 'Post preview'

    class Meta:
        ordering = ['path', ]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Media(models.Model):
    def media_path(instance, filename):
        if instance.uid == None:
            instance.uid = str(uuid.uuid1())
        # ext = filename.split('.')[-1]
        # filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join('media', instance.uid), filename)
    uid = models.TextField(
        max_length=40,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=512,
        default='',
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=512,
        default='',
        blank=True,
        null=True
    )
    media_file = models.FileField(
        'Media file',
        upload_to=media_path,
        blank = True,
        null = True
    )
    is_image = models.BooleanField(
        'Is image',
        default=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=True
    )

    def media_file_preview(self):
        if self.media_file:
            if self.is_image:
                preview = '''
                <table>
                    <tr>
                        <td>
                            <img src="%s?h=100" border="0" title="%s"/>
                        </td>
                        <td>
                            For height limitation: &lt;img src="%s?<b><u>h=100</u></b>" border="0" title="%s"/&gt;<br>
                            For weight limitation: &lt;img src="%s?<b><u>w=100</u></b>" border="0" title="%s"/&gt;<br>
                            For a square picture: &lt;img src="%s?<b><u>s=100</u></b>" border="0" title="%s"/&gt;<br>
                            Link: %s
                        </td>
                    </tr>
                </table>
                ''' % (self.media_file.url, self.description, self.media_file.url, self.description, self.media_file.url, self.description, self.media_file.url, self.description, self.media_file.url)
            else:
                preview = "Link: %s" % self.media_file.url
            return preview
        else:
            return ''

    media_file_preview.short_description = 'Media file'
    media_file_preview.allow_tags = True

    def media_file_admin_preview(self):
        if self.media_file:
            if self.is_image:
                preview = '<img src="%s?s=24" border="0" title="%s"/>' % (self.media_file.url, self.description)
            else:
                preview = '<img src="%s" border="0"/>' % os.path.join(STATIC_URL, 'img/file24.jpg')
            return preview
        else:
            return ''

    media_file_admin_preview.short_description = 'Media'
    media_file_admin_preview.allow_tags = True
