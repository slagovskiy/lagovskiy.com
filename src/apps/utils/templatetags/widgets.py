from django import template


register = template.Library()


@register.inclusion_tag('widgets/tags.html')
def widget_tags():
    return {'tags': '123'}
