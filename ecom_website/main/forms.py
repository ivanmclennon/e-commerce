from django import forms

from .models import Seller


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            "first_name",
            "last_name",
            "email",
            "birthday",
        ]
