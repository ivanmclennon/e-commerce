from datetime import datetime as dt
from typing import Any, Dict, Optional

from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import User

from main.models import Seller


register = template.Library()


@register.simple_tag(takes_context=True)
def seller_from_user(context: Dict[str, Any]) -> Optional[Seller]:
    """
    Return Seller instance from context.user, if authenticated and exists,
    otherwise None.

    :param context: view context
    """
    user: User = context["user"]
    if user.is_authenticated:
        try:
            seller = Seller.objects.get(username=user.username)
        except:
            seller = None
        return seller
    return None


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
