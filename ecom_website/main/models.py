from django.db import models


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
