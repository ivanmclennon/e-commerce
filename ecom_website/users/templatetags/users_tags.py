from typing import Any, Dict, Optional

from django.contrib.auth.models import User
from django import template

from ..models import Seller


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
