from django import template
from apps.blog.models import Category, Tag

register = template.Library()


@register.inclusion_tag('widgets/category.html')
def widget_category():
    categories = Category.objects.all().filter(deleted=False)
    return {'categories': categories}


@register.inclusion_tag('widgets/tags.html')
def widget_tags():
    tags = Tag.objects.all().filter(deleted=False)
    return {'tags': tags}


@register.inclusion_tag('widgets/links.html')
def widget_links():
    return {}
