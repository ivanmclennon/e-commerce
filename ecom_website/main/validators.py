from datetime import date, timedelta

from django.core.exceptions import ValidationError


def age_validator(birthday: date):
    today = date.today()
    age = today.year - birthday.year
    if (today.month < birthday.month) or (
        (today.month == birthday.month) and (today.day < birthday.day)
    ):
        age -= 1
    if age < 18:
        raise ValidationError("You must be over 18 years old to be a seller.")
