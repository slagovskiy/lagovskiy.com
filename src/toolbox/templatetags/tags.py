from django import template
from ..models import Global

register = template.Library()


@register.simple_tag
def make_absoulute_url(val=False):
    if len(str(val)) >= 8:
        if (str(val)[0:7].lower() == 'http://') or (str(val)[0:8].lower() == 'https://'):
            return val
        else:
            return Global.get('site_url') + val
    else:
        return Global.get('site_url') + val
