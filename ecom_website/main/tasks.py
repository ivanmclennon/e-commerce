# Create your tasks here

from celery.app import shared_task

from django.core.mail import send_mass_mail

from .models import Subscriber, ItemListing


@shared_task
def newsletter_task(pk: int) -> None:
    instance: ItemListing = ItemListing.objects.get(pk=pk)
    print(instance)
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
