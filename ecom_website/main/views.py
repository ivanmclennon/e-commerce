from typing import Any, Dict

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import ItemListing, AutoListing, ServiceListing


def index(request):
    return render(request, 'index.html')


# item CBVs
class ItemList(ListView):
    model = ItemListing
    paginate_by = 3


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
