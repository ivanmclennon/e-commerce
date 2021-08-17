from datetime import date

from django import forms
from django.forms.models import inlineformset_factory

from django_countries.widgets import CountrySelectWidget

from .models import (
    Subscriber,
    Picture,
    Seller,
    ItemListing,
    AutoListing,
    ServiceListing,
)


class SellerForm(forms.ModelForm):
    """
    Form for SellerUpdate CBV
    Uses widget for selecting birthday dates within last 100 years
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
    """
    Form for ItemListing CBVs
    Excluded seller and widget for country
    """

    class Meta:
        model = ItemListing
        exclude = ("seller",)
        widgets = {
            "made_in": CountrySelectWidget(),
            "description": forms.widgets.TextInput(),
        }


class AutoForm(forms.ModelForm):
    """
    Form for AutoListing CBVs
    Excluded seller and widget for country
    """

    class Meta:
        model = AutoListing
        exclude = ("seller",)
        widgets = {
            "made_in": CountrySelectWidget(),
            "description": forms.widgets.TextInput(),
        }


# inline formset for adding/editing Picture objects tied to AutoListing
ImageFormset = inlineformset_factory(AutoListing, Picture, fields=("image",), extra=1)


class ServiceForm(forms.ModelForm):
    """
    Form for ServiceListing CBVs
    """

    class Meta:
        model = ServiceListing
        exclude = ("seller",)
        widgets = {
            "description": forms.widgets.TextInput(),
        }


class SubscriberForm(forms.ModelForm):
    """
    Form for subscribing to newsletter
    """

    class Meta:
        model = Subscriber
        fields = ('email',)
