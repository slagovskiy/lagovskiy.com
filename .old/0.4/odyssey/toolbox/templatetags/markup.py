import re
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.filter
def medial_file(value):
    p = re.compile('\%\%img:[A-Za-z0-9-]+[A-Za-z0-9:=]*\%\%')
    m = p.findall(value)
    for _m in m:
        type = ''
        align = 'left'
        param = ''
        uuid = ''
        nolink = False
        border = False
        tmpl = ''
        for __m in _m.replace('%%', '').lower().split(':'):
            if __m == '':
                pass
            elif __m == 'img':
                type = 'img'
            elif __m == 'nolink':
                nolink = True
            elif __m == 'border':
                border = True
            elif __m in ['left', 'right', 'center']:
                align = __m
            elif (__m[0] in ['w', 'h', 's']) and (__m[1] == '='):
                param = __m
            else:
                uuid = __m
        if type == 'img':
            tmpl = render_to_string(
                'media/image_inline.html',
                {
                    'align': align,
                    'param': param,
                    'uuid': uuid,
                    'nolink': nolink,
                    'border': border
                }
            )
        value = value.replace(_m, tmpl)
    return value
