from django.dispatch import receiver
from django.db.models.signals import post_save

from emails.tasks import newsletter_task
from .models import ItemListing


@receiver(post_save, sender=ItemListing)
def notify_new_item(sender, instance, created, **kwargs):
    """
    Calls newsletter_task on new ItemListing saved to db.
    """
    if created:
        newsletter_task(instance.pk)
