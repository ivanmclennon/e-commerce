from typing import Any, Dict
from urllib.parse import urlencode

from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView

from .models import ItemListing, AutoListing, ServiceListing, Listing, Profile


def index(request):
    return render(request, 'index.html')


class BaseListingList(ListView):
    """
    Base ListView class for inheriting
    by Listing's subclasses' CBVs

    :param model: Listing subclass
    :param paginate_by: pagination limit
    """

    model = Listing
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Listing]:
        if 'tag' in self.request.GET:
            return self.model.objects.filter(
                tags__title=self.request.GET['tag']
            )
        return self.model.objects.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = urlencode(query_params)
        return context


class ProfileUpdate(UpdateView):
    model = Profile


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
