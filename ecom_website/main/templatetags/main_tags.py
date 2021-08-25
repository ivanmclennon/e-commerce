from datetime import datetime as dt
from typing import Any, Dict, Optional

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.simple_tag
def current_time(format: str) -> str:
    """
    Return current datetime in specified format.

    :param format: datetime format string
    """
    return dt.now().strftime(format)


@register.simple_tag(takes_context=True)
def query_remainder(context: Dict[str, Any]) -> str:
    """
    Return trailing url query params from context.query_params, if they exist.

    :param context: view context
    """
    if "query_params" in context and context["query_params"]:
        return "&" + context["query_params"]
    return ""


@register.simple_tag(takes_context=True)
def activate_navlink(context: Dict[str, Any], uri: str) -> Optional[str]:
    """
    Return 'active' inside html tag class,
    if website section name (uri) is in request.path (url).

    :param context: view context
    :param uri: website section name
    """
    if uri in context["request"].path:
        return "active"


@register.simple_tag(takes_context=True)
def dynamic_title(context: Dict[str, Any]) -> Optional[str]:
    """
    Capitalized title for the page,
    based on site section name from url path.

    :param context: view context
    """
    request_path = context["request"].path
    sections = ["/items/", "/cars/", "/services/"]
    for section in sections:
        if section in request_path:
            return section.strip("/").capitalize()


@register.filter(name="reversed")
@stringfilter
def custom_reversed(value: str) -> str:
    """
    Returns reversed string.

    :param value: string to reverse
    """
    return value[::-1]
