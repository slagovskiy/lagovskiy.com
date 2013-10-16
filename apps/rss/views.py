# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q

from datetime import date
from datetime import timedelta
from datetime import datetime

import logging

from apps.blog.models import *
from apps.rss.settings import *
from settings_local import DOMAIN_NAME

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.feedgenerator import Atom1Feed

def custom_proc(request):
    return {
        'app_title': 'RSS',
        'link_app': 'rss',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }

class DefaultRSS(Feed):
    feed_type = Rss201rev2Feed
    title = 'Sergey Lagovskiy - blog - last posts'
    link = DOMAIN_NAME + '/rss/'
    description = 'WEB, TECHNOLOGY, DEVELOPMENT, PHOTOGRAPHY, HOME, LIFE'
    language = u'ru-RU'
    ttl = 600
    feed_copyright = 'Copyright (c) 2010-%s, Sergey Lagovskiy' % str(datetime.now().year)

    def categories(self):
        items = []
        for item in Category.objects.all().filter(deleted=False):
            items.append(item.name)
        return items

    def items(self):
        return Post.objects.all().order_by('-published')[:POST_COUNT]

    def item_title(self, item):
        return '<![CDATA[ %s ]]>' % item.title

    def item_description(self, item):
        return '<![CDATA[ %s ]]>' % item.teaser()

    def item_link(self, item):
        return DOMAIN_NAME + item.get_absolute_url()

    def item_author_name(self, item):
        return '%s %s' % (item.author.first_name, item.author.last_name)

    def item_author_email(self, item):
        return item.author.email

    def item_pubdate(self, item):
        return item.published

    def item_categories(self, item):
        items = []
        for item in item.categories.all().filter(deleted=False):
            items.append(item.name)
        return items

class DefaultAtom(DefaultRSS):
    feed_type = Atom1Feed
    link = DOMAIN_NAME + '/atom/'

class TagRSS(DefaultRSS):
    feed_type = Rss201rev2Feed
    title = 'Sergey Lagovskiy - blog - last posts by tag'
    link = DOMAIN_NAME + '/rss/tag/'
    tag = ''

    def get_object(self, request, tag):
        tags = Tag.objects.filter(slug=tag)
        items = []
        if len(tags)>0:
            self.tag = tag
            self.title = 'Sergey Lagovskiy - blog - last posts by tag ' + tags[0].name
            self.link = '/rss/tag/%s/' % tag
            items = Post.objects.filter(status=Post.PUBLISHED_STATUS, tags=tags[0]).order_by('-published')[:POST_COUNT]
        return items

    def items(self, items):
        return items

class TagAtom(TagRSS):
    feed_type = Atom1Feed
    link = DOMAIN_NAME + '/atom/tag/%s/' % TagRSS.tag

class CategoryRSS(DefaultRSS):
    feed_type = Rss201rev2Feed
    title = 'Sergey Lagovskiy - blog - last posts by category'
    link = DOMAIN_NAME + '/rss/category/'
    category = ''

    def get_object(self, request, category):
        categories = Category.objects.filter(slug=category)
        items = []
        if len(categories)>0:
            self.category = category
            self.title = 'Sergey Lagovskiy - blog - last posts by category ' + categories[0].name
            self.link = '/rss/category/%s/' % category
            items = Post.objects.filter(status=Post.PUBLISHED_STATUS, categories=categories[0]).order_by('-published')[:POST_COUNT]
        return items

    def items(self, items):
        return items

class CategoryAtom(CategoryRSS):
    feed_type = Atom1Feed
    link = DOMAIN_NAME + '/atom/category/%s/' % CategoryRSS.category

class CommentsRSS(Feed):
    feed_type = Rss201rev2Feed
    title = 'Sergey Lagovskiy - blog - comments'
    link = DOMAIN_NAME + '/rss/comments/'
    description = 'WEB, TECHNOLOGY, DEVELOPMENT, PHOTOGRAPHY, HOME, LIFE'
    language = u'ru-RU'
    ttl = 600
    feed_copyright = 'Copyright (c) 2010-%s, Sergey Lagovskiy' % str(datetime.now().year)
    post = ''

    def categories(self):
        items = []
        for item in Category.objects.all().filter(deleted=False):
            items.append(item.name)
        return items

    def get_object(self, request, post):
        _post = Post.objects.filter(slug=post)
        items = []
        if len(_post)>0:
            self.post = post
            self.title = 'Sergey Lagovskiy - blog - comments for post ' + _post[0].title
            self.link = '/rss/comments/%s/' % post
            items = Comment.objects.filter(post=_post[0], allowed=True, deleted=False).order_by('-published')
        return items

    def items(self, items):
        return items

    def item_title(self, item):
        return '<![CDATA[ %s ]]>' % item.name

    def item_description(self, item):
        return '<![CDATA[ %s ]]>' % item.content

    def item_link(self, item):
        return DOMAIN_NAME + item.get_absolute_url()

    def item_author_name(self, item):
        return '%s' % item.name

    def item_pubdate(self, item):
        return item.published


class CommentsAtom(CommentsRSS):
    feed_type = Atom1Feed
    link = DOMAIN_NAME + '/atom/comments/%s/' % CommentsRSS.post