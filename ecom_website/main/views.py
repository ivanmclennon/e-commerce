from typing import Any, Dict

from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView, DetailView

from .models import ItemListing, AutoListing, ServiceListing


def index(request):
    return render(request, 'index.html')


class ItemList(ListView):
    model = ItemListing

class ItemDetail(DetailView):
    model = ItemListing

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

class AutoList(ListView):
    model = AutoListing


class ServiceList(ListView):
    model = ServiceListing
