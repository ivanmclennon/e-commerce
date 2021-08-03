from datetime import datetime as dt

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

# custom now
@register.simple_tag
def current_time(format_string):
    return dt.now().strftime(format_string)

# custom reversed
@register.filter(name="reversed")
@stringfilter
def custom_reversed(value):
    return value[::-1]