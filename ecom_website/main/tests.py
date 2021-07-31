from typing import List
from django.test import TestCase
from django.db.models import Model
from django.contrib.auth.models import User

from main.models import Seller, Tag, Category, Listing


def create_model_objects(model_class: Model, kw_list: List[dict]) -> None:
    for kwargs in kw_list:
        obj, created = model_class.objects.get_or_create(**kwargs)
        if not created:
            print(f"{obj} already exists.")


def model_kwargs():
    users_kwargs = [
        {"username": "user2", "password": "123456", "email": "user2@example.com"},
        {"username": "user3", "password": "123456", "email": "user3@example.com"},
        {"username": "user4", "password": "123456", "email": "user4@example.com"},
    ]
    create_model_objects(User, users_kwargs)

    sellers_kwargs = [
        {"user": User.objects.get(username="user1")},
        {"user": User.objects.get(username="user2")},
        {"user": User.objects.get(username="user3")},
        {"user": User.objects.get(username="user4")},
    ]
    create_model_objects(Seller, sellers_kwargs)

    tags_kwargs = [
        {"title": "cheap"},
        {"title": "new"},
        {"title": "used"},
        {"title": "delivery"},
        {"title": "credit"},
    ]
    create_model_objects(Tag, tags_kwargs)

    category_kwargs = [
        {"title": "electronics"},
        {"title": "apparel"},
        {"title": "footwear"},
        {"title": "home and garden"},
        {"title": "beauty and health"},
        {"title": "food and drinks"},
    ]
    create_model_objects(Category, category_kwargs)

    listings_kwargs = [
        {
            "title": "Smart Watch",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="electronics"),
            "seller": Seller.objects.get(user=User.objects.get(username="user1")),
        },
        {
            "title": "T-shirt",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="apparel"),
            "seller": Seller.objects.get(user=User.objects.get(username="user2")),
        },
        {
            "title": "Shovel",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="home and garden"),
            "seller": Seller.objects.get(user=User.objects.get(username="user2")),
        },
        {
            "title": "Toothbrush",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="beauty and health"),
            "seller": Seller.objects.get(user=User.objects.get(username="user3")),
        },
    ]
    create_model_objects(Listing, listings_kwargs)


def print_listings_by_seller():
    for seller in Seller.objects.all():
        print(
            f"{seller.user.username} has a seller profile with "
            f"{seller.count_listings} listings posted."
        )
        for listing in Listing.objects.filter(seller=seller):
            print(f"{listing.title} of category '{listing.category}'")


def print_listings_by_tags():
    for tag in Tag.objects.all():
        print(
            f"{tag.listings.all().count()} listings "
            f"have been tagged with '{tag.title}'"
        )
        for listing in tag.listings.all():
            print(f"{listing.title} of category {listing.category}")
