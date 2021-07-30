import string
import random
from unidecode import unidecode as ud
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
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
