from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Category
from .utils import unique_slug_generator


@receiver(pre_save, sender=Category)
def assign_slug_from_title(sender, instance, *args, **kwargs):
    """
    Creates unique slug attr from Category title pre-save

    :param sender: Category model
    :param instance: Category model instance
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
