from typing import Any, Dict

from django.contrib import messages
from django.http.response import HttpResponse

from main.models import AutoListing, Seller
from main.forms import AutoForm, ImageFormset
from .base import ListingList, ListingDetail, ListingCreate, ListingUpdate


class AutoList(ListingList):
    model = AutoListing
    paginate_by: int = 2


class AutoDetail(ListingDetail):
    model = AutoListing

    # def get_object(self, queryset: Optional[QuerySet] = None) -> AutoListing:
    #     self.object = get_object_or_404(AutoListing, id=self.kwargs["pk"])
    #     return self.object

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Provide last picture to context if car has pictures, otherwise None
        """
        context = super().get_context_data(**kwargs)
        context["picture"] = self.get_object().picture_set.last()
        return context


class AutoCreate(ListingCreate):
    model = AutoListing
    form_class = AutoForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Provides empty formset to context on a GET request
        """
        context = super().get_context_data(**kwargs)
        context["formset"] = ImageFormset()
        return context

    def form_valid(self, form: AutoForm) -> HttpResponse:
        """
        Save car object tied to seller,
        """
        form.instance.seller = Seller.objects.get(pk=self.request.user.pk)
        if form.is_valid():
            car_object: AutoListing = form.save()
            messages.add_message(self.request, messages.SUCCESS, "Listing posted!")

            formset = ImageFormset(
                self.request.POST, self.request.FILES, instance=car_object
            )
            if formset.is_valid():
                formset.save()
        return super().form_valid(form)


class AutoUpdate(ListingUpdate):

    model = AutoListing
    form_class = AutoForm

    def form_valid(self, form: AutoForm) -> HttpResponse:
        formset = ImageFormset(
            self.request.POST, self.request.FILES, instance=self.get_object()
        )
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["formset"] = ImageFormset(instance=self.get_object())
        return context
