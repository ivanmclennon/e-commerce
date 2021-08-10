from typing import Any, Dict, Optional

from django.contrib import messages
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect

from main.models import AutoListing, Seller
from main.forms import AutoForm, ImageFormset
from .base import ListingList, ListingDetail, ListingCreate, ListingUpdate


class AutoList(ListingList):
    model: AutoListing
    paginate_by: int = 2


class AutoDetail(ListingDetail):
    model: AutoListing

    def get_object(self, queryset: Optional[QuerySet] = None) -> AutoListing:
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
    model: AutoListing
    form_class = AutoForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["formset"] = ImageFormset()
        return context

    def form_valid(self, form: AutoForm) -> HttpResponse:
        form.instance.seller = Seller.objects.get(pk=self.request.user.pk)
        if form.is_valid():
            self.object: AutoListing = form.save()
            messages.add_message(self.request, messages.SUCCESS, "Listing posted!")

        formset = ImageFormset(
            self.request.POST, self.request.FILES, instance=self.object
        )
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)


class AutoUpdate(ListingUpdate):

    model: AutoListing
    form_class = AutoForm

    def get_object(self, queryset: Optional[QuerySet] = None) -> AutoListing:
        self.object = get_object_or_404(AutoListing, id=self.kwargs["pk"])
        return self.object

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
