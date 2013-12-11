# -*- coding: utf-8 -*-
import hashlib
from django import template
register = template.Library()

@register.filter
def sha224(value):
    return hashlib.sha224(value).hexdigest()

@register.filter
def sha224f(value):
    v = hashlib.sha224(value).hexdigest()
    return v[0:14] + ':' + v[15:28] + ':' + v[29:42] + ':' + v[43:56]
