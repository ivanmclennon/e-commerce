from django.db import models

from listings.models import AutoListing


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
