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


@register.simple_tag
def get_comment_level(val='', multiplier=1):
    return len(str(val).split('-')) * multiplier


@register.simple_tag
def first(val=['']):
    return val[0]


@register.simple_tag
def top(val=[''], top_cnt=1):
    return val[0:int(top_cnt)]


@register.filter
def date_from_now(val):
    return '<script>\ndocument.write(moment("%s").fromNow());\n</script>' % val


@register.filter
def mul(value, arg):
    return value * arg


@register.filter
def div(value, arg):
    return value / arg


@register.filter
def sub(value, arg):
    return value / arg


@register.filter
def fmul(value, arg):
    return float(value) * float(arg)


@register.filter
def fdiv(value, arg):
    return float(value) / float(arg)


@register.filter
def fsub(value, arg):
    return float(value) / float(arg)
