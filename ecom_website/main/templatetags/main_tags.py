from datetime import datetime as dt

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.simple_tag
def current_time(format_string):
    return dt.now().strftime(format_string)


@register.simple_tag(takes_context=True)
def query_remainder(context):
    if 'query_params' in context and context['query_params']:
        return '&'+context['query_params']
    return ''


@register.filter(name="reversed")
@stringfilter
def custom_reversed(value):
    return value[::-1]
