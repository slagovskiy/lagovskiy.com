# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter
def mul(value, arg):
    '''Умножение'''
    return value * arg

@register.filter
def div(value, arg):
    '''Деление'''
    return value / arg

@register.filter
def sub(value, arg):
    '''Вычитание'''
    return value / arg

@register.filter
def fmul(value, arg):
    '''Умножение'''
    return float(value) * float(arg)

@register.filter
def fdiv(value, arg):
    '''Деление'''
    return float(value) / float(arg)

@register.filter
def fsub(value, arg):
    '''Вычитание'''
    return float(value) / float(arg)
