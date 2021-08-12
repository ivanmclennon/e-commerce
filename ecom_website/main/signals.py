import string
import random

from unidecode import unidecode as ud

from django.utils.text import slugify


def random_string_generator(
    size: int = 10, chars: str = string.ascii_lowercase + string.digits
) -> str:
    """
    Returns random string of needed size.

    :param size: lenght of output string, default 10
    :param chars: set of characters to pick from
    """
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug: str = None) -> str:
    """
    Returns unique slug for Category instance.

    Creates slug from title if new_slug not passed,
    adds random string to slug if created/passed one already exists.

    :param instance: instance of Category model
    :param new_slug: slug to apply
    """
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(ud(instance.title))

    ModelClass = instance.__class__
    qs_exists = ModelClass.objects.filter(slug=slug).exists()

    if qs_exists:
        randstr = random_string_generator(size=4)
        new_slug = f"{slug}-{randstr}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
