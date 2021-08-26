from itertools import chain

from .models import ItemProxy, AutoProxy, ServiceProxy


def get_lastweek_listings() -> list:
    """
    Returns a list of all listing objects posted during last week.
    """
    return list(
        chain(
            ItemProxy.lastweek_objects.all(),
            AutoProxy.lastweek_objects.all(),
            ServiceProxy.lastweek_objects.all(),
        )
    )
