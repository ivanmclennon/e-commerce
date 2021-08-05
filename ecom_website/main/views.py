from typing import Any, Dict, Optional
from urllib.parse import urlencode

from django.shortcuts import render
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView

from .models import ItemListing, AutoListing, ServiceListing, Listing, Seller
from .forms import SellerForm


def index(request):
    return render(request, "index.html")


class BaseListingList(ListView):
    """
    Base ListView class for inheriting
    by Listing's subclasses' CBVs

    :param model: Listing subclass
    :param paginate_by: pagination limit
    """

    model: Listing
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Listing]:
        if "tag" in self.request.GET:
            return self.model.objects.filter(tags__title=self.request.GET["tag"])
        return self.model.objects.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = urlencode(query_params)
        return context


class SellerUpdate(LoginRequiredMixin, UpdateView):
    model = Seller
    # form_class = SellerForm
    fields = ['first_name', 'last_name','email','birthday']
    template_name = "main/seller_update.html"

    def get_object(self, queryset: Optional[QuerySet] = None):
        return self.model.objects.get(pk=self.request.user.pk)


# item CBVs
class ItemList(BaseListingList):
    model = ItemListing
    paginate_by = 3


class ItemDetail(DetailView):
    model = ItemListing


# auto CBVs
class AutoList(BaseListingList):
    model = AutoListing
    paginate_by = 2


class AutoDetail(DetailView):
    model = AutoListing


# service CBVs
class ServiceList(BaseListingList):
    model = ServiceListing
    paginate_by = 2


class ServiceDetail(DetailView):
    model = ServiceListing
