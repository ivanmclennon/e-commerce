from datetime import date

from .models import Seller


def create_default_sellers():
    sellers_kwargs = [
        {
            "username": "user1",
            "email": "user1@example.com",
            "birthday": date(2000, 1, 1),
            "phone_number": "+79991111111",
        },
        {
            "username": "user2",
            "email": "user2@example.com",
            "birthday": date(2000, 1, 1),
            "phone_number": "+79992222222",
        },
        {
            "username": "user3",
            "email": "user3@example.com",
            "birthday": date(2000, 1, 1),
            "phone_number": "+79993333333",
        },
        {
            "username": "user4",
            "email": "user4@example.com",
            "birthday": date(2000, 1, 1),
            "phone_number": "+79994444444",
        },
    ]

    for kwargs in sellers_kwargs:
        obj, created = Seller.objects.get_or_create(**kwargs)
        if not created:
            print(f"{obj} already exists.")
        obj.set_password("123456")
        obj.save()
