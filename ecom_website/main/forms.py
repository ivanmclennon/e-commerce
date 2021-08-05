from datetime import date

from django import forms

from .models import Seller


class SellerForm(forms.ModelForm):
    """
    Form for SellerUpdate CBV
    """

    class Meta:
        model = Seller
        fields = [
            "first_name",
            "last_name",
            "email",
            "birthday",
        ]
        widgets = {
            "birthday": forms.widgets.SelectDateWidget(
                years=range(date.today().year - 100, date.today().year - 17)
            )
        }
