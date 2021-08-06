from typing import Any, Dict, Optional
from urllib.parse import urlencode

from django.shortcuts import render
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from .models import ItemListing, AutoListing, ServiceListing, Listing, Seller
from .forms import SellerForm, ItemForm, AutoForm, ServiceForm


def index(request):
    return render(request, "index.html")


class BaseListingList(ListView):
    """
    Base ListView class for inheriting
    by Listing's subclasses' CBVs

    :param model: Listing subclass
    :param paginate_by: pagination limit
    :param template_name: base template for listviews
    """

    model: Listing
    paginate_by = 10
    template_name = "main/base_listview.html"

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
    """
    Seller model update CBV from UpdateView
    """

    model = Seller
    form_class = SellerForm

    def get_object(self, queryset: Optional[QuerySet] = None):
        return self.model.objects.get(pk=self.request.user.pk)


class ListingCreate(LoginRequiredMixin, CreateView):
    template_name = "main/base_create_form.html"


class ListingUpdate(LoginRequiredMixin, UpdateView):
    template_name = "main/base_update_form.html"


class ItemUpdate(ListingUpdate):

    model = ItemListing
    form_class = ItemForm


class AutoUpdate(ListingUpdate):

    model = AutoListing
    form_class = AutoForm


class ServiceUpdate(ListingUpdate):

    model = ServiceListing
    form_class = ServiceForm


class ItemCreate(ListingCreate):
    model = ItemListing
    form_class = ItemForm

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class AutoCreate(ListingCreate):
    model = AutoListing
    form_class = AutoForm

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class ServiceCreate(ListingCreate):
    model = ServiceListing
    form_class = ServiceForm

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


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
