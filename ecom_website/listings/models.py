from datetime import datetime, timedelta

from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse

from django_countries.fields import CountryField

from users.models import Seller
from main.models import Tag, Category
from .validators import weight_validator


class Listing(models.Model):
    """
    Abstract base model class for listings

    :param title: string title
    :param description: text description
    :param category: foreign key to Category
    :param seller: foreign key to Seller
    :param date_created: auto datetime for object creation
    :param date_modified: auto datetime for object modification
    :param tags: list of applied tags (many-to-many)
    :param price: integer listing price
    """

    title = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    category = models.ForeignKey(
        to=Category, on_delete=models.PROTECT, related_name="%(class)s_set"
    )
    seller = models.ForeignKey(
        to=Seller, on_delete=models.PROTECT, related_name="%(class)s_set"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(to=Tag, related_name="%(class)s_set", blank=True)
    price = models.PositiveIntegerField(default=0, blank=False)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return ""

    class Meta:
        verbose_name = "listing"
        verbose_name_plural = "listings"
        abstract = True


COLOR_CHOICES = (
    ("WHITE", "white"),
    ("BLACK", "black"),
    ("GREY", "grey"),
    ("RED", "red"),
    ("GREEN", "green"),
    ("BLUE", "blue"),
    ("YELLOW", "yellow"),
    ("PURPLE", "purple"),
    ("ORANGE", "orange"),
    ("PINK", "pink"),
)


class ItemListing(Listing):
    """
    Unspecified general item listing class

    :param weight: weight in kg 0.01
    :param made_in: manufacturer country from django-countries
    :param color: item color from COLOR_CHOICES
    """

    # specify validation constraints in the Form
    weight = models.FloatField(validators=(weight_validator,))
    # use CountrySelectWidget in Form
    made_in = CountryField(blank_label="(select country)")
    color = models.CharField(max_length=16, choices=COLOR_CHOICES, default="WHITE")

    def get_absolute_url(self) -> str:
        return reverse("item_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"


class AutoListing(Listing):
    """
    Automobile listing model

    :param weight: weight in kg
    :param made_in: manufacturer country from django-counties
    :param color: item color from COLOR_CHOICES
    :param condition: new/used
    :param mileage: distance traveled in kilometers
    :param picture_set: queryset of assigned Picture images
    """

    # specify validation constraints in the Form
    weight = models.FloatField(validators=(weight_validator,))
    # use CountrySelectWidget in Form
    made_in = CountryField(blank_label="(select country)")
    color = models.CharField(max_length=16, choices=COLOR_CHOICES, default="WHITE")

    CONDITION_CHOICES = (
        ("NEW", "new"),
        ("USED", "used"),
    )

    condition = models.CharField(max_length=8, choices=CONDITION_CHOICES, default="NEW")
    # specify constraints in Form
    mileage = models.PositiveIntegerField(default=0, blank=False)

    picture_set: models.QuerySet

    def get_absolute_url(self) -> str:
        return reverse("car_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "auto"
        verbose_name_plural = "autos"


class ServiceListing(Listing):
    """
    Service listing model

    :param place_type: online/irl
    """

    PLACE_TYPE_CHOICES = (
        ("ONLINE", "online"),
        ("IRL", "in person"),
    )
    place_type = models.CharField(
        max_length=16, choices=PLACE_TYPE_CHOICES, default="IRL"
    )

    def get_absolute_url(self) -> str:
        return reverse("service_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"


class WeeklyListingManager(models.Manager):
    def get_queryset(self) -> QuerySet[Listing]:
        week_ago: datetime = datetime.now() - timedelta(weeks=1)
        return super().get_queryset().filter(date_created__gt=week_ago)


class ItemProxy(ItemListing):

    lastweek_objects = WeeklyListingManager()

    @property
    def email_info(self):
        return f"""
            Item: {self.title}
            Description: {self.description}
            Price: {self.price}
            Link: http://127.0.0.1:8000{self.get_absolute_url()}
            """

    class Meta:
        proxy = True
        ordering = ["date_created"]


class AutoProxy(AutoListing):

    lastweek_objects = WeeklyListingManager()

    @property
    def email_info(self):
        return f"""
            Car: {self.title}
            Description: {self.description}
            Condition: {self.get_condition_display().capitalize()}
            Price: {self.price}
            Link: http://127.0.0.1:8000{self.get_absolute_url()}
            """

    class Meta:
        proxy = True
        ordering = ["date_created"]


class ServiceProxy(ServiceListing):

    lastweek_objects = WeeklyListingManager()

    @property
    def email_info(self):
        return f"""
            Service: {self.title}
            Description: {self.description}
            Type: {self.get_place_type_display().capitalize()}
            Price: {self.price}
            Link: http://127.0.0.1:8000{self.get_absolute_url()}
            """

    class Meta:
        proxy = True
        ordering = ["date_created"]
