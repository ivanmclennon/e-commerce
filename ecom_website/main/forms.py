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


class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemListing
        exclude = ("seller",)
        widgets = {
            "made_in": CountrySelectWidget(),
            "description": forms.widgets.TextInput(),
        }


class AutoForm(forms.ModelForm):
    class Meta:
        model = AutoListing
        exclude = ("seller",)
        widgets = {
            "made_in": CountrySelectWidget(),
            "description": forms.widgets.TextInput(),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceListing
        exclude = ("seller",)
        widgets = {
            "description": forms.widgets.TextInput(),
        }
