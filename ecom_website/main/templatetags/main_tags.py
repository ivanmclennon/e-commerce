from datetime import datetime as dt

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.simple_tag
def current_time(format_string):
    return dt.now().strftime(format_string)


@register.simple_tag(takes_context=True)
def query_remainder(context):
    if "query_params" in context and context["query_params"]:
        return "&" + context["query_params"]
    return ""


@register.simple_tag(takes_context=True)
def activate_navlink(context, uri):
    if uri in context["request"].path:
        return "active"


@register.simple_tag(takes_context=True)
def dynamic_title(context):
    request_path = context["request"].path
    sections = ["/items/", "/cars/", "/services/"]
    for section in sections:
        if section in request_path:
            return section.strip("/").capitalize()


@register.filter(name="reversed")
@stringfilter
def custom_reversed(value):
    return value[::-1]
