from users.tests import create_default_sellers
from emails.tests import create_default_subs

from listings.tests import create_default_listings
from .models import Tag, Category


def create_from_title(model_class, titles):
    for title in titles:
        obj, created = model_class.objects.get_or_create(title=title)
        if not created:
            print(f"{obj} already exists.")


def create_independent_models():

    tags = [
        "cheap",
        "new",
        "used",
        "delivery",
        "credit",
    ]
    create_from_title(Tag, tags)

    categories = [
        "electronics",
        "apparel",
        "footwear",
        "home and garden",
        "beauty and health",
        "food and drinks",
        "vehicles",
        "tutoring",
        "renovation",
        "driving",
    ]
    create_from_title(Category, categories)


def load_default_data():
    create_default_sellers()
    create_default_subs()
    create_independent_models()
    create_default_listings()
