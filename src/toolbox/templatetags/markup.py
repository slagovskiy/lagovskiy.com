import re
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.filter
def medial_file(value):
    p = re.compile('\%\%img:[A-Za-z0-9-]+[A-Za-z0-9:=]*\%\%')
    m = p.findall(value)
    type = ''
    align = 'left'
    param = ''
    uuid = ''
    tmpl = ''
    for _m in m:
        for __m in _m.replace('%%', '').lower().split(':'):
            if __m == 'img':
                type = 'img'
            elif __m in ['left', 'right', 'center']:
                align = __m
            elif (__m[0] in ['w', 'h', 'c']) and (__m[1] == '='):
                param = __m
            else:
                uuid = __m
        if type == 'img':
            tmpl = render_to_string(
                'media/image_inline.html',
                {
                    'align': align,
                    'param': param,
                    'uuid': uuid
                }
            )
        value = value.replace(_m, tmpl)
    return value
