from datetime import datetime, timedelta
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

from django.db.models import QuerySet
from django.core.mail import send_mass_mail

from .models import ItemListing, Subscriber


def stringify_item(item: ItemListing):
    return f"""
    Item: {item.title}
    Description: {item.description}
    Price: {item.price}
    Link: http://127.0.0.1:8000{item.get_absolute_url()}
    """


def make_email(
    to_email: List[str],
    subject: str = "ECOM Newsletter",
    content: str = "You are subscribed.",
    from_email: str = "newsletter@ecom.com",
):
    return (subject, content, from_email, to_email)


def get_letters(items: QuerySet[ItemListing]):

    message_items = "\n\n".join([stringify_item(item) for item in items])

    message_template = f"""
    New listings from last week:

    {message_items}

    You are subscribed to this newsletter.
    """

    subject = "Weekly Items on ECOM"
    messages = [
        make_email([sub.email], subject, message_template)
        for sub in Subscriber.objects.all()
    ]

    return messages


def get_lastweek_items():
    week_ago: datetime = datetime.now() - timedelta(weeks=1)
    new_items: QuerySet[ItemListing] = ItemListing.objects.filter(
        date_created__gt=week_ago
    )
    return new_items


def send_lastweek_items():
    new_items: QuerySet[ItemListing] = get_lastweek_items()

    letters = get_letters(new_items)

    send_mass_mail(letters, fail_silently=False)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_lastweek_items, "interval", weeks=1)
    scheduler.start()
