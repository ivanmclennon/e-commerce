from datetime import date, datetime, timedelta
from typing import TypeVar

from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.contrib.auth.models import User

from django_countries.fields import CountryField

from .validators import age_validator, weight_validator


class Subscriber(models.Model):
    """
    Mailing list subscriber model

    :param email: subscriber's email address
    """

    email = models.EmailField(unique=True, blank=False, null=False)

    class Meta:
        verbose_name = "subscriber"
        verbose_name_plural = "subscribers"


class Seller(User):
    """
    Seller class based on auth.User

    :param birthday: date of birth
    :prop count_listings: number of listings published by seller
    """

    birthday = models.DateField(default=date(2000, 1, 1), validators=(age_validator,))
    avatar = models.ImageField(
        upload_to="main/sellers",
        default="main/sellers/NO_AVATAR.png",
    )

    itemlisting_set: models.QuerySet
    autolisting_set: models.QuerySet
    servicelisting_set: models.QuerySet

    @property
    def count_listings(self) -> int:
        """Count listings published by seller"""
        return (
            self.itemlisting_set.count()
            + self.autolisting_set.count()
            + self.servicelisting_set.count()
        )

    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self) -> str:
        return reverse("seller_update")

    class Meta:
        verbose_name = "seller"
        verbose_name_plural = "sellers"


class Tag(models.Model):
    """
    Listing tag class

    :param title: unique string title
    """

    title = models.CharField(max_length=16, db_index=True, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"


class Category(models.Model):
    """
    Listing category class

    :param title: unique string title
    :param slug: unique auto-created slug from title
    """

    title = models.CharField(max_length=32, db_index=True, unique=True)
    slug = models.SlugField(blank=True, db_index=True, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


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


class Picture(models.Model):
    image = models.ImageField(upload_to="main/cars", default="main/cars/NO_IMAGE.jpg")
    car = models.ForeignKey(
        to=AutoListing, on_delete=models.CASCADE, related_name="%(class)s_set"
    )

    def __str__(self) -> str:
        return self.image.path

    class Meta:
        verbose_name = "picture"
        verbose_name_plural = "pictures"


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
