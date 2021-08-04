from typing import Any, Dict
from urllib.parse import urlencode

from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import ItemListing, AutoListing, ServiceListing, Tag


def index(request):
    return render(request, 'index.html')


# item CBVs
class ItemList(ListView):
    model = ItemListing
    paginate_by = 3

    def get_queryset(self) -> QuerySet[ItemListing]:
        if 'tag' in self.request.GET:
            return ItemListing.objects.filter(
                tags__title=self.request.GET['tag']
            )
        return ItemListing.objects.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = urlencode(query_params)
        return context

class ItemDetail(DetailView):
    model = ItemListing


# auto CBVs
class AutoList(ListView):
    model = AutoListing
    paginate_by = 2


class AutoDetail(DetailView):
    model = AutoListing


# service CBVs
class ServiceList(ListView):
    model = ServiceListing
    paginate_by = 2


class ServiceDetail(DetailView):
    model = ServiceListing
