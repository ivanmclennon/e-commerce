from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

from .utils import age_validator


class Seller(User):
    """
    Seller class based on auth.User

    :param birthday: date of birth
    :param avatar: avatar image
    :param phone_number: phone number
    :prop count_listings: number of listings published by seller
    """

    birthday = models.DateField(default=date(2000, 1, 1), validators=(age_validator,))
    avatar = models.ImageField(
        upload_to="main/sellers",
        default="main/sellers/NO_AVATAR.png",
    )
    # use .as_e164 to get string representation
    phone_number = PhoneNumberField(null=False, blank=False, default="+79991112233")

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
