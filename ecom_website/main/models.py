from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django_countries.fields import CountryField

from .signals import unique_slug_generator


class Seller(User):
    """
    Seller class based on auth.User

    :param birthday: date of birth
    :prop count_listings: number of listings published by seller
    """

    birthday = models.DateField()
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


@receiver(pre_save, sender=Category)
def pre_save_receiver(sender, instance, *args, **kwargs):
    """
    Creates unique slug attr from Category title pre-save

    :param sender: Category model
    :param instance: Category model instance
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


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
    :param made_in: manufacturer country
    :param color: item color from COLOR_CHOICES
    """

    # specify validation constraints in the Form
    weight = models.FloatField()
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
    :param made_in: manufacturer country
    :param color: item color from COLOR_CHOICES
    :param condition: new/used
    :param mileage: distance traveled in kilometers
    """

    # specify validation constraints in the Form
    weight = models.FloatField()
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

    def get_absolute_url(self) -> str:
        return reverse("car_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "auto"
        verbose_name_plural = "autos"


class Picture(models.Model):
    image = models.ImageField()
    car = models.ForeignKey(
        to=AutoListing, on_delete=models.CASCADE, related_name="%(class)s_set"
    )

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


class ItemProxy(ItemListing):
    class Meta:
        proxy = True
        ordering = ["date_created"]


class AutoProxy(AutoListing):
    class Meta:
        proxy = True
        ordering = ["date_created"]


class ServiceProxy(ServiceListing):
    class Meta:
        proxy = True
        ordering = ["date_created"]
