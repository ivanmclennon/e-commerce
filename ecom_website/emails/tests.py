from .models import Subscriber


def create_default_subs():
    emails = [
        "sub1@example.com",
        "sub2@example.com",
    ]

    for email in emails:
        obj, created = Subscriber.objects.get_or_create(email=email)
        if not created:
            print(f"{obj} already exists.")
