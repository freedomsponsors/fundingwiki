# coding=utf-8
from django.template import Library
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

register = Library()

DEFAULT_PAGINATION = settings.PAGINATION_DEFAULT_PAGINATION
DEFAULT_ORPHANS = settings.PAGINATION_DEFAULT_ORPHANS


@register.simple_tag
def add(*args):
    result = 0
    for i in args:
        result += i
    return result


@register.simple_tag
def add_float(ndigits, *args):
    result = 0
    for i in args:
        result += float(i)
    return round(result, ndigits)
