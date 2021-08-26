from typing import List

from users.models import Seller
from main.models import Category
from .models import ItemListing, AutoListing, ServiceListing


def create_listings(model_class, kw_list: List[dict]) -> None:
    for kwargs in kw_list:
        obj, created = model_class.objects.get_or_create(**kwargs)
        if not created:
            print(f"{obj} already exists.")


def create_default_items():
    items_kwargs = [
        {
            "title": "Smart Watch",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="electronics"),
            "seller": Seller.objects.get(username="user1"),
            "weight": 0.05,
            "color": "BLACK",
            "made_in": "CHN",
            "price": 200,
        },
        {
            "title": "T-shirt",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="apparel"),
            "seller": Seller.objects.get(username="user2"),
            "weight": 0.08,
            "color": "WHITE",
            "made_in": "FRA",
            "price": 50,
        },
        {
            "title": "Shovel",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="home and garden"),
            "seller": Seller.objects.get(username="user2"),
            "weight": 1.55,
            "made_in": "RUS",
            "price": 100,
        },
        {
            "title": "Toothbrush",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="beauty and health"),
            "seller": Seller.objects.get(username="user3"),
            "weight": 0.15,
            "color": "BLUE",
            "made_in": "DEU",
            "price": 150,
        },
        {
            "title": "Smartphone",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="electronics"),
            "seller": Seller.objects.get(username="user4"),
            "weight": 0.15,
            "color": "BLUE",
            "made_in": "CHN",
            "price": 500,
        },
        {
            "title": "Pizza knife",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="home and garden"),
            "seller": Seller.objects.get(username="user4"),
            "weight": 0.1,
            "color": "RED",
            "made_in": "ITA",
            "price": 20,
        },
    ]
    create_listings(ItemListing, items_kwargs)


def create_default_autos():
    autos_kwargs = [
        {
            "title": "Mercedes AMG",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="vehicles"),
            "seller": Seller.objects.get(username="user1"),
            "weight": 2000.0,
            "color": "BLUE",
            "made_in": "DEU",
            "price": 50000,
            "condition": "NEW",
            "mileage": 0,
        },
        {
            "title": "BMW X5",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="vehicles"),
            "seller": Seller.objects.get(username="user1"),
            "weight": 2500.0,
            "color": "BLACK",
            "made_in": "DEU",
            "price": 60000,
            "condition": "USED",
            "mileage": 1000,
        },
        {
            "title": "VAZ 2104",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="vehicles"),
            "seller": Seller.objects.get(username="user2"),
            "weight": 1500.0,
            "color": "GREEN",
            "made_in": "RUS",
            "price": 1000,
            "condition": "USED",
            "mileage": 15000,
        },
        {
            "title": "Go-kart",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="vehicles"),
            "seller": Seller.objects.get(username="user3"),
            "weight": 200.0,
            "color": "RED",
            "made_in": "FRA",
            "price": 5000,
            "condition": "NEW",
            "mileage": 0,
        },
        {
            "title": "Huyndai Solaris",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="vehicles"),
            "seller": Seller.objects.get(username="user4"),
            "weight": 1200.0,
            "color": "WHITE",
            "made_in": "KOR",
            "price": 40000,
            "condition": "USED",
            "mileage": 123,
        },
        {
            "title": "Kia Rio",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="vehicles"),
            "seller": Seller.objects.get(username="user4"),
            "weight": 1200.0,
            "color": "YELLOW",
            "made_in": "KOR",
            "price": 45000,
            "condition": "NEW",
            "mileage": 0,
        },
    ]
    create_listings(AutoListing, autos_kwargs)


def create_default_services():
    services_kwargs = [
        {
            "title": "Teach Python",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="tutoring"),
            "seller": Seller.objects.get(username="user1"),
            "price": 10,
            "place_type": "ONLINE",
        },
        {
            "title": "Window installation",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="renovation"),
            "seller": Seller.objects.get(username="user2"),
            "price": 200,
            "place_type": "IRL",
        },
        {
            "title": "Personal driver",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="driving"),
            "seller": Seller.objects.get(username="user3"),
            "price": 100,
            "place_type": "IRL",
        },
        {
            "title": "Personal stylist",
            "description": "lorem ipsum",
            "category": Category.objects.get(title="tutoring"),
            "seller": Seller.objects.get(username="user3"),
            "price": 50,
            "place_type": "ONLINE",
        },
    ]
    create_listings(ServiceListing, services_kwargs)


def create_default_listings():
    create_default_items()
    create_default_autos()
    create_default_services()
