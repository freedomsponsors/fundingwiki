from django import template
from apps.issues.services import language_services

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def lang_name(code):
    """concatenate arg1 & arg2"""
    return language_services.get_language_name_from_code(code)