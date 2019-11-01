from ...blog.models import Category, Tag
from django import template
from ...info.models import Link

register = template.Library()


@register.inclusion_tag('widgets/category.html')
def widget_category(active_category=''):
    categories = Category.objects.all().filter(deleted=False)
    return {
        'categories': categories,
        'active_category': active_category
    }


@register.inclusion_tag('widgets/tags.html')
def widget_tags(active_tag=''):
    tags = Tag.objects.all().filter(deleted=False)
    return {
        'tags': tags,
        'active_tag': active_tag
    }

@register.inclusion_tag('widgets/links.html')
def widget_links():
    links = Link.objects.all().filter(deleted=False).order_by('order')
    return {'links': links}

'''
@register.inclusion_tag('widgets/album.html')
def widget_albums(active_album=''):
    albums = Album.objects.all().filter(deleted=False)
    return {
        'albums': albums,
        'active_album': active_album
    }


@register.inclusion_tag('widgets/device.html')
def widget_device_types(active_device_type=''):
    device_types = DeviceType.objects.all().filter(deleted=False, show_in_menu=True)
    return {
        'device_types': device_types,
        'active_device_type': active_device_type
    }


@register.inclusion_tag('widgets/phototags.html')
def widget_phototags(active_phototag=''):
    phototags = PhotoTag.objects.all().filter(deleted=False)
    return {
        'phototags': phototags,
        'active_phototag': active_phototag
    }


@register.inclusion_tag('widgets/links.html')
def widget_links():
    mylinks = MyLink.objects.all().filter(deleted=False)
    return {'mylinks': mylinks}


@register.inclusion_tag('widgets/archive.html')
def widget_archive():
    return {'archives': ['2016', '2015', '2014', '2013']}
'''
