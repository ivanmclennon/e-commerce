from abc import ABC

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django_countries.fields import CountryField

from .signals import unique_slug_generator


class Seller(User):

    @property
    def count_listings(self) -> int:
        """Count listings published by seller"""
        return self.listings.all().count()

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'seller'
        verbose_name_plural = 'sellers'


class Tag(models.Model):
    title = models.CharField(
        max_length=16,
        db_index=True,
        unique=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class Category(models.Model):
    title = models.CharField(
        max_length=32,
        db_index=True,
        unique=True
    )
    slug = models.SlugField(
        blank=True,
        db_index=True,
        unique=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


@receiver(pre_save, sender=Category)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Listing(models.Model):
    title = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name='listings'
    )
    seller = models.ForeignKey(
        to=Seller,
        on_delete=models.PROTECT,
        related_name='listings'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        to=Tag,
        related_name='listings',
        blank=True
    )
    price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'listing'
        verbose_name_plural = 'listings'
        abstract = True


COLOR_CHOICES = (
    ('WHITE', 'white'),
    ('BLACK', 'black'),
    ('GREY', 'grey'),
    ('RED', 'red'),
    ('GREEN', 'green'),
    ('BLUE', 'blue'),
    ('YELLOW', 'yellow'),
    ('PURPLE', 'purple'),
    ('ORANGE', 'orange'),
    ('PINK', 'pink'),
)


class ItemListing(Listing):
    """
    Unspecified general item class.
    :param weight: weight in kg 0.01
    :param made_in: manufacturer country
    :param color: item color
    """

    # specify validation constraints in the Form
    weight = models.FloatField()
    # use CountrySelectWidget in Form
    made_in = CountryField(blank_label='(select country)')
    color = models.CharField(
        max_length=16,
        choices=COLOR_CHOICES,
        default="WHITE"
    )

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'


class AutoListing(Listing):

    # specify validation constraints in the Form
    weight = models.FloatField()
    # use CountrySelectWidget in Form
    made_in = CountryField(blank_label='(select country)')
    color = models.CharField(
        max_length=16,
        choices=COLOR_CHOICES,
        default="WHITE"
    )

    class Condition(models.TextChoices):
        NEW = 'NEW', _('New')
        USED = 'USED', _('Used')

    condition = models.CharField(
        max_length=8,
        choices=Condition.choices,
        default=Condition.NEW
    )
    # specify constraints in Form
    mileage = models.IntegerField()

    class Meta:
        verbose_name = 'auto'
        verbose_name_plural = 'autos'


class ServiceListing(Listing):

    PLACE_TYPE_CHOICES = (
        ('ONLINE', 'online'),
        ('IRL', 'in person'),
    )
    place_type = models.CharField(
        max_length=16,
        choices=PLACE_TYPE_CHOICES,
        default='IRL'
    )

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'


class ListingProxy(Listing):
    class Meta:
        proxy = True
        ordering = ["date_created"]
