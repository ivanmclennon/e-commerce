from datetime import date

from django.core.exceptions import ValidationError


def age_validator(birthday: date) -> None:
    today = date.today()
    age = today.year - birthday.year
    if (today.month < birthday.month) or (
        (today.month == birthday.month) and (today.day < birthday.day)
    ):
        age -= 1
    if age < 18:
        raise ValidationError("You must be over 18 years old to be a seller.")


def weight_validator(weight: float) -> None:
    if weight < 0.01 or weight > 9999.99:
        raise ValidationError("Weight must be between 0.01 and 9999.99")
