from django.db import models

from listings.models import AutoListing


class Picture(models.Model):
    image = models.ImageField(upload_to="cars", default="cars/NO_IMAGE.jpg")
    car = models.ForeignKey(
        to=AutoListing, on_delete=models.CASCADE, related_name="%(class)s_set"
    )

    def __str__(self) -> str:
        return self.image.path

    class Meta:
        verbose_name = "picture"
        verbose_name_plural = "pictures"
