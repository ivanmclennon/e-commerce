from typing import Optional

from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from main.models import Seller
from main.forms import SellerForm


class SellerUpdate(LoginRequiredMixin, UpdateView):
    """
    UpdateView for updating Seller's information
    """

    model = Seller
    form_class = SellerForm

    def get_object(self, queryset: Optional[QuerySet] = None) -> Seller:
        return self.model.objects.get(pk=self.request.user.pk)
