from django import forms

from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    """
    Form for subscribing to newsletter
    """

    class Meta:
        model = Subscriber
        fields = ("email",)
