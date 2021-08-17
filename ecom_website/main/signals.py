from datetime import datetime as dt

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Group
from django.core.mail import send_mail

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


@receiver(post_save, sender=Seller)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        message = f"""
        Hello, {instance.username}!
        Welcome to our website!
        Sent at: {dt.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        send_mail(
            subject="Welcome to ECOM!",
            from_email="hifemay304@hax55.com",
            message=message,
            recipient_list=[instance.email],
            fail_silently=False,
        )
