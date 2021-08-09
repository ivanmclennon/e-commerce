from typing import Any, Dict, Optional
from urllib.parse import urlencode
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from .models import ItemListing, AutoListing, ServiceListing, Listing, Seller, Picture
from .forms import SellerForm, ItemForm, AutoForm, ServiceForm, ImageFormset


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


class ServiceUpdate(ListingUpdate):

    model = ServiceListing
    form_class = ServiceForm


class ItemCreate(ListingCreate):
    model = ItemListing
    form_class = ItemForm

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

    def get_object(self):
        self.object = get_object_or_404(AutoListing, id=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            pic = AutoListing.objects.get(pk=self.kwargs["pk"]).picture_set.last()
        except:
            pic = None
        context["picture"] = pic
        return context


class AutoCreate(ListingCreate):
    model = AutoListing
    form_class = AutoForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["formset"] = ImageFormset()
        return context

    def form_valid(self, form: AutoForm) -> HttpResponseRedirect:
        form.instance.seller = Seller.objects.get(pk=self.request.user.pk)
        if form.is_valid():
            self.object: AutoListing = form.save()
            messages.add_message(self.request, messages.SUCCESS, "Listing posted!")

        formset = ImageFormset(
            self.request.POST, self.request.FILES, instance=self.object
        )
        if formset.is_valid():
            formset.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class AutoUpdate(ListingUpdate):

    model = AutoListing
    form_class = AutoForm

    def get_object(self, queryset=None) -> AutoListing:
        return get_object_or_404(AutoListing, pk=self.kwargs["pk"])

    def form_valid(self, form: AutoForm) -> HttpResponse:
        form.instance.seller = Seller.objects.get(pk=self.request.user.pk)
        formset = ImageFormset(
            self.request.POST, self.request.FILES, instance=self.get_object()
        )
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["formset"] = ImageFormset()
        try:
            pic = AutoListing.objects.get(pk=self.kwargs["pk"]).picture_set.last()
        except:
            pic = None
        context["picture"] = pic
        return context


# service CBVs
class ServiceList(BaseListingList):
    model = ServiceListing
    paginate_by = 2


class ServiceDetail(DetailView):
    model = ServiceListing
