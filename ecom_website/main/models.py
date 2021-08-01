from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .signals import unique_slug_generator


class Seller(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.PROTECT,
        primary_key=True
    )

    @property
    def count_listings(self) -> int:
        """Count listings published by seller"""
        return self.listings.all().count()

    def __str__(self) -> str:
        return self.user.username

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

    class Meta:
        verbose_name = 'listing'
        verbose_name_plural = 'listings'
