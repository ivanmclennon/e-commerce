import string
import random

from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Category


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    ModelClass = instance.__class__
    qs_exists = ModelClass.objects.filter(slug=slug).exists()

    if qs_exists:
        randstr = random_string_generator(size=4)
        new_slug = f"{slug}-{randstr}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Category)
def create_slug_on_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
