from django.db import models


class Subscriber(models.Model):
    """
    Mailing list subscriber model

    :param email: subscriber's email address
    """

    email = models.EmailField(unique=True, blank=False, null=False)

    class Meta:
        verbose_name = "subscriber"
        verbose_name_plural = "subscribers"
