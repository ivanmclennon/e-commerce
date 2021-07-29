from django.test import TestCase
from django.db.models import Model
from django.contrib.auth.models import User

from main.models import Seller, Tag, Category, Listing


def create_model_object(model_class: Model, **kwargs) -> Model:
    obj = model_class(**kwargs)
    return obj


users_kwargs = [
    {"username": "user2", "password": "123456", "email": "user2@example.com"},
    {"username": "user3", "password": "123456", "email": "user3@example.com"},
    {"username": "user4", "password": "123456", "email": "user4@example.com"},
]

sellers_kwargs = [
    {"user": User.objects.get(username="user1")},
    {"user": User.objects.get(username="user2")},
    {"user": User.objects.get(username="user3")},
    {"user": User.objects.get(username="user4")},
]

tags_kwargs = [
    {"title": "cheap"},
    {"title": "new"},
    {"title": "used"},
    {"title": "delivery"},
    {"title": "credit"},
]

category_kwargs = [
    {"title": "electronics"},
    {"title": "apparel"},
    {"title": "footwear"},
    {"title": "home and garden"},
    {"title": "beauty and health"},
    {"title": "food and drinks"},
]

listings_kwargs = [
    {
        "title": "Smart Watch",
        "description": "lorem ipsum",
        "category": Category.objects.get(title="electronics"),
        "seller": Seller.objects.get(user=User.objects.get(username="user1")),
        "tags": Tag.objects.filter(title__in=['new', 'cheap'])
    },
    {
        "title": "T-shirt",
        "description": "lorem ipsum",
        "category": Category.objects.get(title="apparel"),
        "seller": Seller.objects.get(user=User.objects.get(username="user2")),
        "tags": Tag.objects.filter(title__in=['delivery', 'cheap'])
    },
    {
        "title": "Shovel",
        "description": "lorem ipsum",
        "category": Category.objects.get(title="home and garden"),
        "seller": Seller.objects.get(user=User.objects.get(username="user2")),
        "tags": Tag.objects.filter(title__in=['used'])
    },
    {
        "title": "Toothbrush",
        "description": "lorem ipsum",
        "category": Category.objects.get(title="beauty and health"),
        "seller": Seller.objects.get(user=User.objects.get(username="user3")),
        "tags": Tag.objects.filter(title__in=['new', 'delivery'])
    },
]
