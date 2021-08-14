from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Group

from .models import Seller, Category
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


@receiver(post_save, sender=Seller)
def assign_common_user_group(sender, instance, created, **kwargs):
    if created:
        group_name = "common users"
        group_obj, created = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group_obj)
