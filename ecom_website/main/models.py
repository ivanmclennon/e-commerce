from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    @property
    def count_listings(self):
        return self.listings.objects.count()


class Tag(models.Model):
    title = models.CharField(max_length=16)


class Category(models.Model):
    title = models.CharField(max_length=32)
    slug = models.SlugField(auto_created=True)


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    seller = models.ForeignKey(
        to=Seller,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        to=Tag,
        related_name='listings'
    )
