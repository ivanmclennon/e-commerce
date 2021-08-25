from typing import Any, Dict
from urllib.parse import urlencode

from django.contrib import messages
from django.shortcuts import render
from django.urls.base import reverse
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from users.views import CheckUserRightsMixin
from ..models import Listing, Seller
from ..forms import SubscriberForm


def index(request: HttpRequest) -> HttpResponse:
    """
    Render index.html template
    Includes newsletter subscriber form
    """
    subscriber_form = SubscriberForm()
    return render(
        request,
        "index.html",
        {
            "form": subscriber_form,
        },
    )


def subscribe_view(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = SubscriberForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Subscribed to newsletter!")
        else:
            messages.error(
                request, f"Cannot subscribe with email: {form.cleaned_data.email}"
            )
    return HttpResponseRedirect(reverse("index"))


class ListingList(ListView):
    """
    Base class for displaying a list of listings

    :param model: Listing subclass
    :param paginate_by: pagination limit
    :param template_name: base template for listviews
    """

    model: Listing
    paginate_by: int = 10
    template_name: str = "main/base_listview.html"

    def get_queryset(self) -> QuerySet[Listing]:
        """
        Filters by tag if "tag" is in query_params.
        Order by 'date_created'
        """
        if "tag" in self.request.GET:
            return self.model.objects.filter(
                tags__title=self.request.GET["tag"]
            ).order_by("date_created")
        return self.model.objects.all().order_by("date_created")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Cleans 'page' query param between requests for pagination
        """
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = urlencode(query_params)
        return context


class ListingCreate(CheckUserRightsMixin, CreateView):
    """
    Base class for creating a listing
    Overwrite 'model' and 'form_class' to use with Listing's subclasses

    :param template_name: base template for creating
    """

    template_name: str = "main/base_create_form.html"

    def form_valid(self, form) -> HttpResponse:
        """
        Fills seller field in created listing with current user's seller acccount
        """
        form.instance.seller = Seller.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class ListingUpdate(LoginRequiredMixin, UpdateView):
    """
    Base class for updating a listing

    :param template_name: base template for updating
    """

    template_name: str = "main/base_update_form.html"


class ListingDetail(DetailView):
    """
    Base class for displaying a listing
    """

    pass
