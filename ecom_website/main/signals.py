from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Category, ItemListing
from .utils import unique_slug_generator
from emails.tasks import newsletter_task


@receiver(post_save, sender=ItemListing)
def notify_new_item(sender, instance, created, **kwargs):
    """
    Calls newsletter_task on new ItemListing saved to db.
    """
    if created:
        newsletter_task(instance.pk)


@receiver(pre_save, sender=Category)
def assign_slug_from_title(sender, instance, *args, **kwargs):
    """
    Creates unique slug attr from Category title pre-save

    :param sender: Category model
    :param instance: Category model instance
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
