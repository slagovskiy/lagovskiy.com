from django import template
from apps.blog.models import Tag

register = template.Library()


@register.inclusion_tag('widgets/tags.html')
def widget_tags():
    tags = Tag.objects.all().filter(deleted=False)
    return {'tags': tags}
