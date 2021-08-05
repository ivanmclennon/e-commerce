from datetime import date

from django import forms

from django_countries.widgets import CountrySelectWidget

from .models import Seller, ItemListing, AutoListing, ServiceListing


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


class ListingForm(forms.ModelForm):
    class Meta:
        fields = [
            "title",
            "description",
            "category",
            "price",
            "tags",
        ]


class ItemForm(forms.ModelForm):
    """
    Form for creating/updating ItemListing
    """

    class Meta(ListingForm.Meta):
        model = ItemListing
        fields = [
            "weight",
            "made_id",
            "color",
        ]
        widgets = {"made_in": CountrySelectWidget()}
