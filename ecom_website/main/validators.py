from django.core.exceptions import ValidationError


def weight_validator(weight: float) -> None:
    """
    Raises ValidationError if weight is outside of (0.01, 9999.99) range
    """
    if weight < 0.01 or weight > 9999.99:
        raise ValidationError("Weight must be between 0.01 and 9999.99")
