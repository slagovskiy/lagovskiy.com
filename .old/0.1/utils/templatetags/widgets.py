# -*- coding: utf-8 -*-
import logging
from django import template

register = template.Library()

def widget_categories_menu():
    categories = []
    try:
        from apps.blog.models import Category
        categories = Category.objects.all().order_by('sort', 'name').exclude(deleted=True)
    except:
        logging.exception('Error in widget widget_categories_menu')
    return {'categories': categories}

def widget_tags_menu():
    tags = []
    try:
        from apps.blog.models import Tag
        tags = Tag.objects.all().order_by('sort', 'name').exclude(deleted=True)
    except:
        logging.exception('Error in widget widget_tags_menu')
    return {'tags': tags}

def widget_banners():
    banners = []
    try:
        from apps.banner.models import Banner
        banners = Banner.objects.all().order_by('sort').exclude(deleted=True)
    except:
        logging.exception('Error in widget widget_banner')
    return {'banners': banners}

def widget_archive_menu():
    dates = {}
    try:
        from apps.blog.models import Post
        for item in Post.objects.filter(status=Post.PUBLISHED_STATUS).dates('published','year',order='DESC'):
            dates[item] = Post.objects.filter(status=Post.PUBLISHED_STATUS, published__year=item.year).dates('published','month',order='DESC')
    except:
        logging.exception('Error in widget widget_archive_menu')
    return {'dates': dates}

def widget_admin_menu():
    return {}

def widget_links_menu():
    return {}

register.inclusion_tag('widgets/categories.html')(widget_categories_menu)
register.inclusion_tag('widgets/tags.html')(widget_tags_menu)
register.inclusion_tag('widgets/links.html')(widget_links_menu)
register.inclusion_tag('widgets/admin.html')(widget_admin_menu)
register.inclusion_tag('widgets/banners.html')(widget_banners)
register.inclusion_tag('widgets/archive.html')(widget_archive_menu)
