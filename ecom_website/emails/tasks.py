from celery import shared_task

from django.core.mail import send_mass_mail

from main.models import ItemProxy
from main.utils import get_lastweek_listings
from .models import Subscriber


@shared_task
def weekly_newsletter_task():
    listings = get_lastweek_listings()

    message_items = "\n\n".join([listing.email_info for listing in listings])

    content = f"""
        New listings from last week:

        {message_items}

        You are subscribed to this newsletter.
        """

    subject = "Last week's listings on ECOM"
    from_email = "newsletter@ecom.com"

    messages = [
        (subject, content, from_email, [sub.email]) for sub in Subscriber.objects.all()
    ]

    send_mass_mail(messages, fail_silently=False)


@shared_task
def newsletter_task(pk: int) -> None:
    instance: ItemProxy = ItemProxy.objects.get(pk=pk)
    message_template = f"""
        New listing has just been published!

        {instance.title}
        {instance.description}
        {instance.price}

        You are subscribed to this newsletter.
    """
    subject = "New Item on ECOM"
    from_email = "newsletter@ecom.com"
    messages = []

    for sub in Subscriber.objects.all():
        message = (subject, message_template, from_email, [sub.email])
        messages.append(message)

    send_mass_mail(messages, fail_silently=False)
